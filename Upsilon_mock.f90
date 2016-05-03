!July 2. Added FFT (to compute correlation function)
!        +  Coyote (to compute Non-linear power spectrum) 
!Upsilon Module, last update Jun 17

module Upsilon
use cmbdata
use cmbtypes
use constants
use Precision
use likelihood
use Spline
implicit none

type, extends(CosmologyLikelihood) :: UpsLikelihood
   contains
   procedure :: LogLike => Ups_LnLike
end type UpsLikelihood


integer :: use_upsilon
integer :: upsilon_option
logical :: use_coyote
logical :: use_XiAB
logical :: remove_pairs
logical :: virgin=.True.

! Params that describe the files of the mocks
integer :: mock_NP, mock_gg
logical :: use_mock
logical :: use_diag
real :: R0_gg, R0_gm, z_gg, z_gm, aver 
character*100  mock_file
character*100  mock_cov
character*100  best_fit

character*100, dimension(10000) :: lines
character*100 bchi2name
integer nlines


type UpsilonData
   real :: ggR0, gmR0, zdatagg, zdatagm, calibamp, calibcor
   integer :: NP
   logical, allocatable, dimension (:) :: isgg
   real, allocatable, dimension (:) :: rra, dsups
   real(dl), allocatable, dimension (:,:) :: cov, icov

   !! We really use this just to pass parameters around, it changes
   !! and it is not intrinsic part of data
   integer bselector  !! bfuncselector
   real :: bias, biasp, biaspp
   real :: min_ggR0
end type UpsilonData


type(UpsilonData), target :: DLRG, DDEBUG
type(UpsilonData), pointer :: Dcur
type(CSpline) :: thc_Fid, thc_ns, thc_s8p, thc_s8m, thc_oml,thc_omh,thc_ah,thc_al, thc_h0l, thc_h0h
type(CSpline) :: GalPtA, GalPtB
type(CSpline) :: CoyoSpl, FFTSpl, FFTSpl_0, FFTSpl_1, FFTSpl_2, FFTSpl_3, FFTSpl_4
type(CSpline) :: PkSpl, PkASpl, PkBSpl, PkkSpl, XilinSpl, Xi_ASpl, Xi_BSpl 

                                
real, parameter :: zdatafid = 0.23, maxrgg=100.0, maxrgm=100.0 ! 150, 150,zfid=0.23
!be the actual redshift of simulations. 
real, parameter :: finalcor =0.00
integer, parameter :: MAXNP=200
real*8 :: pi_ = 4*ATAN(1d0)
real*8, parameter :: alnkmin=log(1d-4), alnkmax=log(10d0), alnkmin2=log(1d-4), alnkmax2=log(20d0)
real :: bestchi2=1e30
real :: deltabiasp

integer, parameter  :: numr= 304  !Stop there

    contains

    subroutine UpsLikelihood_Add(LikeList, Ini)
       use IniFile
       use settings
       class(LikelihoodList) :: LikeList
       Type(TIniFile) :: ini
       Type(UpsLikelihood), pointer :: like


       if (Ini_Read_Logical_File(Ini, 'use_Ups',.false.)) then
          allocate(like)
          like%LikelihoodType = 'Ups'
          like%needs_background_functions = .true.
          call LikeList%Add(like)
          if (Feedback>1) write(*,*) 'read Ups datasets'
       end if
    end subroutine UpsLikelihood_Add


    function Ups_LnLike(like, CMB, Theory, DataParams)
       implicit none
       Class(CMBParams) CMB
       Class(UpsLikelihood) :: like
       Class(TheoryPredictions) Theory
       real(mcp) :: DataParams(:)
       real(mcp) Ups_LnLike, UpsilonLike
       real DSXR02 !! the 
       real bias, biasp, biaspp,cross_corr, ds3, rhobar, biase
       real lbias, lbiasp, lbiaspp, mbias, mbiasp, mbiaspp
       integer ii
       real, dimension(MAXNP) :: theo, diff
       real chi2, chi2c,zdata, factor
       real  rl, t1 ,t2, rad

       type (CSpline) :: XiSpl, SigmaGG, SigmaGM, GetGG, GetGM
       integer, parameter :: NR = 150 !// from 100 before
       real, dimension (NR) :: xirr,xival, xival0,xival2, xilin, xi2lin, thgg, thgm
       real :: minr, maxr, corrfact, alphacross, gfactgg, gfactgm
       real :: gfactgg0, gfactgm0, s8, ryr, upscalib
       real*8, external :: rombint
       character*100 tmpstr
       integer nsets, bits
       integer bfuncselector
       character*16 idstr
       real rt, fftb
       integer ki, ini_set   
       real*8 kk, h0, test1, kka

        
       integer, parameter  :: nn = 582 !Maximum # cause of the fft code
       double precision x(7), y(1164) 
       real, dimension (582):: new_k, new_pk, k_lin, pk_lin 
       integer t(1)

       real*8 ru(numr), fftlog(numr) 

       integer, parameter  :: nq = 20
       real, dimension (nq):: new_q, new_pqa, new_pqb, new_Pkk

       if (virgin.and.use_upsilon<101) then
          call InitUpsilon
          virgin=.False.
       end if

        !Non-linear Theory
       if (use_coyote) then 
          print *,'Using Coyote emulator'
          x(1) =   CMB%ombh2               ! omega_b 
          x(2) =   CMB%omdmh2+ CMB%ombh2   ! omega_m
          x(3) =   CMB%InitPower(1)        ! n_s
          x(4) =   CMB%H0
          x(5) =   -1.000                  ! w
          x(6) =   Theory%sigma_8          ! sigma8
          x(7) =   z_gg                    ! redshift
   
          t(1) = 2                         ! 1= D^2, 2= P(k)        
       
          call emu(x,y,t)

          h0 = CMB%H0/100.0
          do ii=1, nn
             new_k(ii)  = y(ii)/h0
             new_pk(ii) = y(ii+ nn)*h0**3.0

          enddo   
          call CoyoSpl%init(new_k, new_pk)
          call IniFFT(ru, fftlog, CMB,Theory, 0)
          call FFTSpl%init(REAL(ru), REAL(fftlog))
       end if

        ! Linear Theory
       do ki = 1,nn
          k_lin(ki) = exp(alnkmin+(ki-1)*(alnkmax-alnkmin)/(nn-1.0))
          pk_lin(ki) = MatterPowerat_Z(Theory,DBLE(k_lin(ki)), z_gg*1.0_dl)
       end do

       call PkkSpl%init(k_lin, pk_lin)

       minr = 1. !2.0  
       maxr = 150 !150.0

       do ii = 1, NR
          xirr(ii) = minr * (maxr/minr)**(DBLE((ii-1))/DBLE((NR-1)))
          xilin(ii) =  Xi(DBLE(xirr(ii)), CMB,Theory, z_gg*1.0_dl, 0.d0)
          xi2lin(ii) = (xilin(ii))**2.
       end do

       call XilinSpl%init(xirr, xilin)
       call Xi_BSpl%init(xirr, xi2lin) 

        !Xi_AB
       if (use_XiAB) then
          do ki = 1, nq
             new_q(ki)  = exp(alnkmin2 +(ki-1)*(alnkmax2 - alnkmin2)/(nq-1.0))
             new_pqa(ki) =  Pk_AB(DBLE(new_q(ki)), z_gg*1.0_dl, 0)
             ! new_pqb(ki) =  Pk_AB(DBLE(new_q(ki)), z_gg*1.0_dl, 1) 
          end do

          call PkASpl%init(REAL(new_q), REAL(new_pqa))
          call IniFFT(ru, fftlog, CMB,Theory, 1)
          call Xi_ASpl%init(REAL(ru), REAL(fftlog))  

                ! Double check that give same value with F2=1 and xi**@
          !call PkASpl%init(REAL(new_q), REAL(new_pqb))
          !call IniFFT(ru, fftlog, CMB,Theory,  2)
          !call Xi_BSpl%init(REAL(ru), REAL(fftlog))
       end if

       !-----------

        !Check this number, for mocks should be one
       !rhobar =  2.77519737e11*(CMB%omdm+CMB%omb+0.0*CMB%omnu)*1e-12
       rhobar =  CMB%hola*0.01
       !print *, 'rhobar',rhobar !, CMB%hola 

       s8       = Theory%sigma_8
       upscalib = CMB%upscalib

       DLRG%bias   = CMB%upsdata(10) !/s8
       DLRG%biasp  = CMB%upsdata(11)
       DLRG%biaspp = CMB%upsdata(12) 
 

       do ii = 1, NR
          rad      = minr * (maxr/minr)**(DBLE((ii-1))/DBLE((NR-1)))
          xirr(ii) = rad
          if (use_coyote) then
             xival0(ii) = FFTSpl%eval(real(rad))
          else
             xival0(ii) = XilinSpl%eval(real(rad))             
          end if   
       end do



          !-- Use only for printing purposes
         if (use_upsilon .eq. 101 .and. use_coyote) then  
            open (50,file='test_Pk.dat')
              do ki = 1,nn
                 kk = exp(alnkmin+(ki-1)*(alnkmax-alnkmin)/(nn-1.0))
                 write (50,'(3G)'), kk, PkkSpl%eval(real(kk)), CoyoSpl%eval(real(kk)) 
              end do
            close(50)

            open (51,file='test_Xi.dat')
              do ii = 1, NR
                 rad = minr * (maxr/minr)**(DBLE((ii-1))/DBLE((NR-1)))
                 write (51,'(3G)'),  rad, XilinSpl%eval(real(rad)), FFTSpl%eval(real(rad))
              end do
            close(51)


            if (use_XiAB) then  
             open (52,file='test_Xi_Afid2.dat')
               do ii = 1, NR
                  rad = minr * (maxr/minr)**(DBLE((ii-1))/DBLE((NR-1)))
                  write (52,'(3G)'), rad, Xi_ASpl%eval(real(rad)),Xi_BSpl%eval(real(rad))                
               end do
             close(52)     
            end if 
         end if
          !-----

       chi2=0
       bits=1
                        ! Here is where the mocks are read
       DCUR => DLRG

       chi2c = GetDataChi2(DCUR)
       chi2  = chi2+chi2c
       bits  = bits*2

       print *, 'nsets -> ',chi2c
       print *, 'chi2 before calibration', chi2
       chi2 = chi2 !+ (upscalib**2)/1.**2 !! unit calibration error

       UpsilonLike = (chi2)/2.0  !! no minus is cosmomc.

         !-------------------
       Ups_LnLike=UpsilonLike
       print *, 'Ups_Lnlike',Ups_LnLike
    
    contains

       function GetDataChi2 (D) result (chx2)
          type (UpsilonData) :: D
          real chx2

          bias   = D%bias
          biasp  = D%biasp
          biaspp = D%biaspp
          bfuncselector = D%bselector
             

 
          if (use_coyote) then
             gfactgg= 1.
             gfactgm= 1.
          else
             gfactgg=MatterPowerat_Z(Theory,0.01_dl,D%zdatagg*1.0_dl)/MatterPowerat_Z(Theory,0.01_dl,zdatafid*1.0_dl)
             gfactgm=MatterPowerat_Z(Theory,0.01_dl,D%zdatagm*1.0_dl)/MatterPowerat_Z(Theory,0.01_dl,zdatafid*1.0_dl)
          end if

       
          if (use_XiAB) then 
             gfactgg0= 1.
             gfactgm0= 1.             
          else 
             gfactgg0= MatterPowerat_Z(Theory,0.01_dl,D%zdatagg*1.0_dl)/MatterPowerat_Z(Theory,0.01_dl,0.0_dl)
             gfactgm0= MatterPowerat_Z(Theory,0.01_dl,D%zdatagm*1.0_dl)/MatterPowerat_Z(Theory,0.01_dl,0.0_dl)
          end if
 
!print *,'gfactor', (s8/0.8)**4*gfactgg0**2, gfactgg0**2


          minr = 1. !2.0     
          maxr = 150. !150.0   

          do ii=1,NR
             rad      = minr * (maxr/minr)**(DBLE((ii-1))/DBLE((NR-1)))
             xirr(ii) = rad
                 
             if (use_coyote) then
                 xival(ii) = xival0(ii) * 1.0
             else
                if (upsilon_option.ne.1.and.upsilon_option.ne.2) then
                   xival(ii) = xival0(ii)*XiCorr(CMB,Theory,xirr(ii),(D%zdatagg+D%zdatagm)/2.0)
                     print *, 'Xi', rad, xival(ii), FFTSpl%eval(real(rad))
                else if (upsilon_option.eq.1) then
                   xival(ii) = xival0(ii) * XiCorr(CMB,Theory,xirr(ii),zdatafid)                    
                else if (upsilon_option.eq.2) then
                   xival(ii) = xival0(ii) * 1.0
                end if
             end if
          end do

          call XiSpl%init(xirr,xival)

          do ii=1, NR
             rad = minr * (maxr/minr)**(DBLE((ii-1))/DBLE((NR-1)))
             xirr(ii)   = rad
             xival(ii)  = 2*rombint(dsggfunc, 0d0, DBLE(maxrgg), 1d-5)
             xival2(ii) = 2*rombint(dsgmfunc, 0d0, DBLE(maxrgm), 1d-5)
          end do

          call SigmaGG%init(xirr, xival)
          call SigmaGM%init(xirr, xival2)

          do ii=1, NR
             rad = minr * (maxr/minr)**(DBLE((ii-1))/DBLE((NR-1)))
             xirr(ii) = rad
             thgg(ii) = GetUpsilon(SigmaGG, rad ,D%ggR0)         
             thgm(ii) = GetUpsilon(SigmaGM, rad ,D%gmR0)
          end do

          call GetGG%init(xirr, thgg)
          call GetGM%init(xirr, thgm)

          factor = 1.0 !rhobar*(1.0+upscalib*D%calibamp)*D%calibcor

          do ii=1,D%NP
             rad = D%rra(ii)
             if (D%isgg(ii)) then
               theo(ii)= (GetGG%eval(rad-aver)+GetGG%eval(rad)+GetGG%eval(rad+aver))/3.0
             else
               theo(ii)= (GetGM%eval(rad-aver)+GetGM%eval(rad)+GetGM%eval(rad+aver))*factor/3.0
             end if
          end do

             !-- print best_fit
            if (use_upsilon .eq. 99) then
               open (53,file= best_fit)
                  do ii=1,int(D%NP)
                     write (53,*)D%rra(ii),D%dsups(ii),sqrt(D%cov(ii,ii)), theo(ii)
                  end do
               close(53)
            end if

            if (use_upsilon .eq. 99 .and. not (use_XiAB)) then
             open (53,file='test_Tobias_XA.dat')
                do ii = 1, NR
                  rad = minr * (maxr/minr)**(DBLE((ii-1))/DBLE((NR-1)))
                  write (53,'(3G)'),  rad, GalPtA%eval(rad)*(s8/0.8)**4 *gfactgg0**2, GalPtB%eval(rad)*(s8/0.8)**4 * gfactgg0**2
                  !write (53,'(3G)'),  rad, GalPtA%eval(rad), GalPtB%eval(rad) 
             end do
             close(53)
            end if



          diff(1:D%NP) = theo(1:D%NP) - D%dsups
          chx2 = DOT_PRODUCT(diff(1:D%NP),MATMUL(D%icov,diff(1:D%NP)))
       end function GetDataChi2


       real*8 function dsggfunc (x)
          real*8 x
          real tr, xi, xi_A, xi_B
          real b2
          tr= sqrt(rad**2+x**2)
          xi = XiSpl%eval (tr) * gfactgg

          if (use_XiAB) then
            xi_A = Xi_ASpl%eval(tr)
            xi_B = Xi_BSpl%eval(tr)
          else
            xi_A = GalPtA%eval(tr)*(s8/0.8)**4 * gfactgg0**2
            xi_B = GalPtB%eval(tr)*(s8/0.8)**4 * gfactgg0**2
          end if

            ! We should fix b_hh to b_hm+0.2
          b2= biasp !+deltabiasp
            ! if (tr>3.96 .and.tr<4) write(*,'(10G)') tr, xi, bias, s8, xi*bias**2 
          dsggfunc = xi * bias**2  +  2*bias*b2*xi_A  +  b2**2 * xi_B
       end function dsggfunc


       real*8 function dsgmfunc(x)
          real*8 x
          real tr, xi, xi_A
          tr= sqrt(rad**2+x**2)
         xi = XiSpl%eval (tr) * gfactgm

          if (use_XiAB) then
            xi_A = Xi_ASpl%eval(tr)
          else        
            xi_A = GalPtA%eval(tr)*(s8/0.8)**4 * gfactgm0**2 
          end if

            !!    write (66,*) tr, bias , 1/xi*(biasp * gfactgm0**2 * GalPtA%eval(tr) *(s8/0.8)**4) 
            !! gfactgm is the growth factor squared
          dsgmfunc = xi * bias  +  biasp * xi_A
       end function dsgmfunc

    end function Ups_LnLike


    subroutine InitUpsilon
       integer ii, jj, NX
       real :: tmp(1000,11)
       real :: excal
       
       deltabiasp=0.0
       print *, "Using: zdatafid:",zdatafid, "maxrgg:", maxrgg,"maxrgm:",maxrgm

       call LoadUpsilonData(DLRG, mock_file, mock_cov, mock_NP, mock_gg, R0_gg, R0_gm, z_gg, z_gm, 1.0,0.04, 1, use_diag)

       DLRG%min_ggR0 = R0_gg
       open (50, file='NLcorrXi_all.dat', status='old')
          read(50,*) NX
          if (NX>1000) stop 'bad shit'
             do ii=1,NX
                read (50,*) tmp(ii,1:11)
             end do
       close(50)

       call thc_Fid%init(tmp(1:NX,1), tmp(1:NX,2))
       call thc_ns%init(tmp(1:NX,1), tmp(1:NX,3))
       call thc_s8p%init(tmp(1:NX,1), tmp(1:NX,4))
       call thc_s8m%init(tmp(1:NX,1), tmp(1:NX,5))
       call thc_oml%init(tmp(1:NX,1), tmp(1:NX,6))
       call thc_omh%init(tmp(1:NX,1), tmp(1:NX,7))

       call thc_ah%init(tmp(1:NX,1), tmp(1:NX,8))
       call thc_al%init(tmp(1:NX,1), tmp(1:NX,9))

       call thc_h0l%init(tmp(1:NX,1), tmp(1:NX,10))
       call thc_h0h%init(tmp(1:NX,1), tmp(1:NX,11))

       if (not (use_XiAB))  call LoadGalPt
    end subroutine InitUpsilon



    subroutine LoadUpsilonData (D, fnamedat, fnamecov, NP, NPGG, ggR0, gmR0,zdatagg, zdatagm, calibcor, calibamp, bs,ZeroOffDiag)
       integer NP, ii, jj, NPGG
       real ggR0, gmR0, calibcor, calibamp
       real zdatagg, zdatagm
       character*(*) fnamedat, fnamecov
       type (UpsilonData) :: D
       logical ZeroOffDiag
       integer bs

       print *,"Loading:", TRIM(fnamedat),',', TRIM(fnamecov)
       print *, 'Using only diagonal', ZeroOffDiag
       allocate (D%isgg(NP), D%rra(NP), D%dsups(NP), D%cov(NP,NP), D%icov(NP,NP))
       D%ggr0 = ggr0
       D%gmr0 = gmr0
       D%np = np
       D%bselector = bs
       D%zdatagg = zdatagg
       D%zdatagm = zdatagm
       D%calibamp = calibamp
       D%calibcor = calibcor
         !! first open data gg data
       open (50, file =fnamedat, status='old')
          do ii=1,NP
             read (50,*) D%rra(ii), D%dsups(ii)
          end do
       close(50)

       open (50, file =fnamecov, status='old')
          do ii=1,NP
             read (50,*) D%cov(ii,1:NP)
          end do 
       close(50)


       if (ZeroOffDiag) then
          do ii=1,NP
             do jj=1,NP
               if (Ii.ne.jj) D%cov(ii,jj)=0
             end do
          end do
       end if


       D%isgg(1:NPGG) = .true.
       D%isgg(NPGG+1:NP) = .false.
       D%icov=D%cov 

       call Matrix_Inverse(D%icov)


       if (.false.) then 
          print *,'----------------------------:',fnamedat
          print *,'At the end of LoadUpsilonData we have'
          print *, 'calibamp=',D%calibamp, 'calibcor=',D%calibcor
          print *, 'zdatagg=',zdatagg, 'zdatagm=',zdatagm
          print *, 'rad:', D%rra
          print *, 'ups:', D%dsups
          print *, 'COV:', D%cov
       end if
    end subroutine LoadUpsilonData


    subroutine LoadGalPt
       integer, parameter :: NP=1500
       real, DIMENSION(NP) :: r,a,b
       real  tmp
       integer ii


       open (144,file='galpt.dat',status='old')
          do ii=1,NP
             read (144,*) r(ii), tmp, a(ii), b(ii)
          end do
       close(144) 
         !! see Tobias' email
!       a=a*2
!       b=b*2

       call GalPtA%init(r, a)
       call GalPtB%init(r, b)

    end subroutine LoadGalPt


 
       !This function in now improved and substitute by Coyote
    real*8 function Xi (ru, CMB, Theory, curz, q)
       implicit none
       real*8 ru, q
       real(dl) curz
       Type (CMBParams) CMB
       Type(TheoryPredictions) Theory
       real*8, external :: rombint

       Xi = rombint (xifunc, alnkmin, alnkmax, 1d-5)/(2*pi_**2)

       contains
       real*8 function xifunc (alnk)
          use specfun
          real*8 alnk, ak,x, pow

          ak=exp(alnk)
          x=ak*ru

          pow = PkkSpl%eval(real(sqrt(ak**2+q**2)))/(1+finalcor)**2 

          xifunc = pow*sin(x)/x * ak**3   !=3, cause using log
       end function xifunc
   end function Xi



    real*8 function Pk_AB (k, curz, ab)
       implicit none
       integer ab
       real(dl) k, curz, k_in
       real*8, external :: rombint

        Pk_AB = rombint (xifunc, -1d0, 1d0, 1d-2) !1d-2 use this
        contains
         real*8 function xifunc (u)
           real*8 u
           xifunc = Int_q (k, curz, u, ab)
        end function xifunc

    end function Pk_AB




    real*8 function Int_q (k, curz, u, ab)
        implicit none
        integer ab
        real(dl) k, u, curz
        real(dl) kdiff_min, kdiff_max
        real*8, external :: rombint
        
        Int_q = rombint (xifunc, alnkmin2 , alnkmax2 , 1d-3)/(4*pi_**2) !1d-3 use this
                                              
        contains
        real*8 function xifunc (alnq)
                real(dl) alnq, pow, F2, q, kmq, k_in
               
                q    = exp(alnq)
                kmq  = k*u -q
                k_in = k**2 + q**2 - 2.0*k*q*u
 
                 if (sqrt(k_in) < exp(0.5*alnkmin2) .or. sqrt(k_in)> exp(alnkmax2*0.5) .or. k_in ==0) then
                     pow = 0
                 else
                     if (ab == 0)  then 
                        F2  = 5./7. + kmq*(0.5d0*k**2 - 5*q*kmq/7.)/(q*k_in) 
                     else
                        F2  = 1.0
                     end if
                     
                     pow = PkkSpl%eval(real(sqrt(k_in)))*F2*PkkSpl%eval(real(q))
                 end if

        xifunc = pow* q**3 
        end function xifunc
    end function Int_q   

    
!!=--------------------------------------------
!It's better to integrate in theta and then in q
       !Integral in q
    real*8 function Xi_B (k, Theory, curz)
       implicit none
       Type(TheoryPredictions) Theory
       real(dl) curz, k
       real*8, external :: rombint

       Xi_B =  rombint (xifunc, alnkmin2 , alnkmax2 , 1d-4)/(4*pi_**2)
                                                     !5d-4
       contains
       real*8 function xifunc (alnq)
          real*8 alnq, aq, pow

          aq     = exp(alnq) 
          !pow    = MatterPowerat_Z(Theory,DBLE(aq),curz) * Xi_A (k, Theory, curz, aq )   
          pow = PkkSpl%eval(real(aq)) * Xi_del (k, Theory, curz, aq )
          xifunc = pow* aq**3   !=3, cause using log
       end function xifunc
   end function Xi_B

       !Integral in theta
    real*8 function Xi_del (k, Theory, curz, q)
       implicit none
       Type(TheoryPredictions) Theory
       real*8 q, k
       real(dl) curz, pow, k_in
       real*8, external :: rombint

        Xi_del = rombint (xifunc, -1d0, 1d0, 3d-2)
       contains
       real*8 function xifunc (u)
          real*8 u, pow, F2

          k_in  = k**2 + q**2 - 2.0*k*q*u
          if (sqrt(k_in) <= exp(alnkmin2)) then
              pow = 0
          else
              F2  = 5./7. + (k*u -q)/(q*(k_in))*((5./7.)*q*(q - k*u) + 0.5d0*k**2)
              pow = PkkSpl%eval(real(sqrt(k_in)))* F2
          end if
          xifunc = pow
       end function xifunc
     end function Xi_del

!-------------------------------------


 
       !This function in now improved and substitute by Coyote 
    real function XiCorr(CMB,Theory, rad, zz) Result (C)
       implicit none
       Type (CMBParams) CMB
       Type(TheoryPredictions) Theory
       real rad
       real zz, H0, M_nu
       real aa, aafid, nseff
       real, parameter :: H0_fid=70
       if (rad.gt.50) then
          C=1.0
          return
       end if


       H0 = CMB%H0;
       M_nu =CMB%omnuh2*93.14  ! neutrino mass in eV. This is accurate enough for correction
       nseff = CMB%InitPower(1) !!!! we now heave exact derivatives- 0.01*M_nu/0.15
                                        !+(H_0-H_0_fid)/H_0_fid

       C = 1.0
       C = C +thc_ns%eval(rad)*(nseff-1.0) !! ns
       if (upsilon_option.ne.10) then
          if (Theory%sigma_8.gt.0.8) then
             C = C +thc_s8p%eval(rad)*(Theory%sigma_8-0.8) !! s8
          else
             C = C +thc_s8m%eval(rad)*(Theory%sigma_8-0.8) !! s8
          end if
       end if

       if ((CMB%omb+CMB%omdm).gt.0.25) then
          C = C + thc_omh%eval(rad)*( (CMB%omb+CMB%omdm)-0.25)  !!omega_m
       else
          C = C + thc_oml%eval(rad)*( (CMB%omb+CMB%omdm)-0.25)  !!omega_m
       end if

       if (H0.gt.H0_fid) then
          C = C + thc_h0h%eval(rad)*( H0-H0_fid )  !!H0hi
       else
          C = C + thc_h0l%eval(rad)*( H0-H0_fid )  !!H0lo
       end if

       aa=1./(1.+zz);
       aafid=1/(1.+0.23);
       if (zdatafid.ne.0.23) print *, "WARN:zdatafid"


       if (aa.gt.aafid) then
          C = C + thc_ah%eval(rad) * (aa-aafid)
          !   print *, aa, aafid, rad,(1+thc_ah%eval(rad) * (aa-aafid)),'A'
       else if (aa.lt.aafid) then
       C = C + thc_al%eval(rad) * (aa-aafid)
          !    print *, aa, aafid, rad,(1+thc_al%eval(rad) * (aa-aafid)),'B'
       end if

          !print *, rad, C,'O', (CMB%initpower(1)-1.0), (info%theory%sigma_8-0.8), ((CMB%omb+CMB%omdm)-0.25)

       C = C*thc_Fid%eval(rad)
    end function XiCorr



    function GetUpsilon (Sigma, rad, R0) Result (res)
       implicit none
       type (CSpline) :: Sigma
       real :: rad, res, R0
       real*8, external :: rombint

       res = 2/rad**2* rombint (upsfunc, DBLE(R0), DBLE(rad),1d-5)
       res = res - Sigma%eval(rad) + Sigma%eval(R0)*R0**2/rad**2

       contains
         real*8 function upsfunc(x)
            real*8 x
            upsfunc = Sigma%eval(REAL(x)) * x
         end function upsfunc
    end function GetUpsilon


    subroutine IniFFT(ru, fftlog, CMB, Theory,  what) 
      implicit none   
      Type(TheoryPredictions) Theory
      Type (CMBParams) CMB

      integer NMAX
      logical ok
      parameter (NMAX=4096)
      integer dir,i,kropt,n 
      real*8 a(NMAX), dlnr,dlogr,k,kr,logkc,logrc,logrmax,logrmin
      real*8  mu,nc,q,r,rk
      real*8 wsave(2*NMAX+3*(NMAX/2)+19)

      integer, parameter:: nnm = 304  !Stop there
      integer what 
      real*8 kk(nnm), Pkk(nnm), kx(nnm) 
      real*8 rx 

      parameter (n = numr) 
      real*8 ru(numr), fftlog(numr)  
     
      logrmin = -6.  
      logrmax =  2. !1.5  
      mu   = 0.5d0
      q    = 0.0d0
      kr   = 0.5d0  
      kropt= 3  
      dir  = 1

      logrc=(logrmin+logrmax)/2.d0
      nc=dble(n+1)/2.d0
      dlogr=(logrmax-logrmin)/n
      dlnr=dlogr*log(10.d0)

      kx(1)     = log10(1d-5)  
      kx(nnm)   = log10(1d3) 
      Pkk(1)    = 0  
      Pkk(nnm)  = 0     
 
      do i = 2, nnm -1 
        if (what.eq.0) then
             kk(i)  = exp(alnkmin+(i-2.0)*(alnkmax-alnkmin)/(nnm-3.0)) 
             Pkk(i) = CoyoSpl%eval(real(kk(i)))
        else  if (what.eq.1) then                  
             kk(i)  = exp(alnkmin2 +(i-2.0)*(alnkmax2 - alnkmin2)/(nnm-3.0))
             Pkk(i) = PkASpl%eval(real(kk(i))) 
        else
             kk(i)  = exp(alnkmin2 +(i-2.0)*(alnkmax2 - alnkmin2)/(nnm-3.0))
             Pkk(i) = PkBSpl%eval(real(kk(i)))
        end if

        kx(i)  = log10(kk(i))
      end do
      
      call PkSpl%init(real(kx), real(Pkk))  
 
      do i=1,n 
         r   = 10.d0**(logrc+(i-nc)*dlogr)
         rx  = log10(r)
         a(i)= PkSpl%eval(real(rx))*(r/(2*3.1416))**1.5
      enddo

        !initialize FFTLog transform - note fhti resets kr
      call fhti(n,mu,q,dlnr,kr,kropt,wsave,ok)
      if (.not.ok) stop
      logkc=log10(kr)-logrc
      call fht(n,a,dir,wsave)

      do i=1,n
        ru(i)    = 10.d0**(logkc+(i-nc)*dlogr)
        fftlog(i)= a(i)/(ru(i)**1.5)
      enddo
    end subroutine
    
end module Upsilon
