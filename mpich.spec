%define	name	mpich
%define	version 1.2.5.2
%define release	%mkrel 10
%define	lib_name_orig	lib%{name}
%define	lib_major	1
%define	lib_name	%mklibname %{name} %{lib_major}
%define	mpihome		%{_localstatedir}/mpi

Name: 		%{name}
Summary: 	MPICH is a portable implementation of MPI
Version: 	%{version}
Release: 	%{release}
Source0: 	%{name}-%{version}.tar.bz2
Source1: 	rhosts.mpi
Source2:	test_mpi.c
Patch0: 	%{name}-1.2.5-sysconfdir.patch.bz2
Patch1: 	%{name}-1.2.5-datadir.patch.bz2
Patch2:		%{name}-1.2.5-all.patch.bz2
Patch3:		%{name}-1.2.5-mpiinstall.patch.bz2
Patch4:		%{name}-1.2.5.2-fix-bug8697.patch.bz2
Patch5:		%{name}-1.2.5.2-fix-bug8713.patch.bz2
Patch6:		%{name}-1.2.5.2-skip-rsh-check.patch.bz2
Patch7:		%{name}-1.2.5-mpiinstall-lib64.patch.bz2
Patch8:		%{name}-1.2.5-mpeinstall-lib64.patch.bz2
URL: 		http://www-unix.mcs.anl.gov/mpi/mpich/
License:	BSD-style 
Group: 		System/Cluster
Requires: 	rsh, xinetd, rsh-server, %{lib_name} = %{version}-%{release}
PreReq:		rpm-helper
BuildRequires:	gcc >= 3.2, gcc3.3-g77 >= 3.2

%description
MPICH is a freely available, portable implementation of MPI, the Standard 
for message-passing libraries.
MPICH-A Portable Implementation of MPI is a MPI Standard conforming library 
that was developed by the Argonne National Laboratory. It allows different 
processes across a network of workstations to communicate using specific 
message passing functions. It includes libraries, parallel debugging tools 
and docs.

This package provides the libraries that use the standard p4 device.

%package -n	mpich-doc
Summary:	Documentation for developing programs that will use MPICH
Group:		Development/Other

%description -n mpich-doc
MPICH is a freely available, portable implementation of MPI, the Standard 
for message-passing libraries.
MPICH-A Portable Implementation of MPI is a MPI Standard conforming library 
that was developed by the Argonne National Laboratory. It allows different 
processes across a network of workstations to communicate using specific 
message passing functions. It includes libraries, parallel debugging tools 
and docs.

This package provides the documentation needed to develop
applications using the MPICH libraries.

%package -n	%{lib_name}
Summary:	Shared Libraries for MPICH
Group:		Development/Other
Provides:	%{lib_name}

%description  -n %{lib_name}
Shared Libraries for MPICH

%package -n	%{lib_name}-devel
Summary:	Headers for developing programs that will use MPICH
Group:		Development/Other
Requires:	mpich = %{version}-%{release}, %{lib_name} = %{version}-%{release}
Provides:	%{lib_name}-devel
Provides:	%name-devel

%description -n %{lib_name}-devel
MPICH is a freely available, portable implementation of MPI, the Standard 
for message-passing libraries.
MPICH-A Portable Implementation of MPI is a MPI Standard conforming library 
that was developed by the Argonne National Laboratory. It allows different 
processes across a network of workstations to communicate using specific 
message passing functions. It includes libraries, parallel debugging tools 
and docs.

This package provides the static libraries and header files needed to compile
applications using the MPICH libraries.

%package -n	mpicc
Summary:	The MPICH wrapper over the C compiler
Group:		Development/C
Requires:	gcc >= 3.2, %{lib_name}-devel = %{version}-%{release}

%description -n mpicc
MPICH is a freely available, portable implementation of MPI, the Standard 
for message-passing libraries.
MPICH-A Portable Implementation of MPI is a MPI Standard conforming library 
that was developed by the Argonne National Laboratory. It allows different 
processes across a network of workstations to communicate using specific 
message passing functions. It includes libraries, parallel debugging tools 
and docs.

This package provides the shell script mpicc, with headers, which allows to
compile C programs using the MPICH libraries.

%package -n	mpic++
Summary:	The MPICH wrapper over the C++ compiler
Group:		Development/C++
Requires:	gcc-c++ >= 3.2, %{lib_name}-devel = %{version}-%{release}

%description -n mpic++
MPICH is a freely available, portable implementation of MPI, the Standard 
for message-passing libraries.
MPICH-A Portable Implementation of MPI is a MPI Standard conforming library 
that was developed by the Argonne National Laboratory. It allows different 
processes across a network of workstations to communicate using specific 
message passing functions. It includes libraries, parallel debugging tools 
and docs.

This package provides the shell script mpiCC, with headers, which allows to
compile C++ programs using the MPICH libraries.

%package -n	mpif77
Summary:	The MPICH wrapper over the Fortran 77 compiler
Group:		Development/Other
Requires:	gcc3.3-g77 >= 3.2, %{lib_name}-devel = %{version}-%{release}

%description -n mpif77
MPICH is a freely available, portable implementation of MPI, the Standard 
for message-passing libraries.
MPICH-A Portable Implementation of MPI is a MPI Standard conforming library 
that was developed by the Argonne National Laboratory. It allows different 
processes across a network of workstations to communicate using specific 
message passing functions. It includes libraries, parallel debugging tools 
and docs.

This package provides the shell script mpif77, with headers, which allows to
compile Fortran 77 (NOT Fortran 90!) programs using the MPICH libraries.


%prep
%setup -q
%patch0 -p1 
%patch1 -p1
#a%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p1 -b .peroyvind
%patch7 -p0 
%patch8 -p0

find -name .cvsignore | xargs rm -rf
find -name CVS -type d | xargs rm -rf

%pre
/usr/sbin/groupadd -g 12384 -r -f mpi > /dev/null 2>&1 ||:
/usr/sbin/useradd -u 12384 -g mpi -d %{mpihome} -r -s /bin/bash mpi -p "" -m > /dev/null 2>&1 ||:

%postun
%_postun_userdel mpi

%post
STATUS=$(cat /etc/xinetd.d/rsh  | grep disable | cut -d "=" -f 2)
if [ $STATUS == "yes" ]; then
echo "Warning !!"
echo "The rsh daemon is disabled in your xinetd config file(/etc/xinetd.d/rsh), please activate it."
fi
echo "Remember that you should create a .rhosts in your home directory."
echo "Look at .rhosts in the doc directory for a sample configuration"
echo "A mpi user has been created, change it's home directory to a network file system with the other nodes"

# automatically set mpi variable
TEST_MPI_ENV=`grep MPI /etc/bashrc`
if [ -z "$TEST_MPI_ENV" ] ; then
	echo "# MPI environment" >> /etc/bashrc
	echo "MPIRUN_HOME=/usr/bin" >> /etc/bashrc
	echo "export MPIRUN_HOME" >> /etc/bashrc
fi


%build
CFLAGS=$RPM_OPT_FLAGS; export CFLAGS;
[ -f configure.in ] && libtoolize --copy --force;

./configure --prefix=%{_prefix} \
        --exec-prefix=%{_exec_prefix} \
        --bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
        --datadir=%{_datadir}/mpich/ \
        --includedir=%{_includedir} \
	--libdir=%{_libdir} \
        --sharedstatedir=%{_sharedstatedir} \
	--docdir=%{_datadir}/doc/%{name}-%{version} \
	--htmldir=%{_datadir}/doc/%{name}-%{version}/www \
        --mandir=%{_mandir} \
 	--sharedlib=%{_libdir} \
        --enable-c++ \
        --enable-f77 \
        --with-arch=LINUX \
        --with-device=ch_p4 \
        --with-comm=ch_p4 \
        --enable-sharedlib \
 	--enable-debug \
	--disable-weak-symbols \
	--without-java

make


%install
rm -rf $RPM_BUILD_ROOT

export MPICH_INCLUDE_PROFLIB="yes"

#Changing libdir for compilators
for i in $(ls $RPM_BUILD_DIR/%{name}-%{version}/bin/mpi*); do
perl -pi -e "s|libdir=/usr/lib|libdir=$RPM_BUILD_ROOT/usr/lib|" $i
done

#Patching UseSharedLib for using libmpichfarg by default
perl -pi -e 's|UseSharedLib\=\$\{MPICH_USE_SHLIB\-no\}|UseSharedLib\=yes|' $RPM_BUILD_DIR/%{name}-%{version}/bin/mpif77
perl -pi -e 's|UseSharedLib\=\$\{MPICH_USE_SHLIB\-no\}|UseSharedLib\=yes|' $RPM_BUILD_DIR/%{name}-%{version}/src/fortran/src/mpif77


#Patching prefix for mpd
#perl -pi -e "s|exec_prefix \=.*|exec_prefix \=$RPM_BUILD_ROOT/usr/|" $RPM_BUILD_DIR/%{name}-%{version}/mpid/mpd/Makefile


make install "PREFIX=$RPM_BUILD_ROOT%{_prefix}\
	     -sysconfpath=$RPM_BUILD_ROOT/%{_sysconfdir}/mpich/ \
	     -datapath=$RPM_BUILD_ROOT/%{_datadir}/mpich/ \
	     -shliblocal=$RPM_BUILD_ROOT/%{_libdir} \
	     -soft"


#Changing back libdir for compilators
for i in $(ls $RPM_BUILD_ROOT/usr/bin/mpi*); do
perl -pi -e "s|libdir=$RPM_BUILD_ROOT/usr/lib|libdir=/usr/lib|" $i
done

#Activiating PMPI patches
for i in $(ls $RPM_BUILD_DIR/%{name}-%{version}/bin/*); do
perl -pi -e 's|MPI_WITH_PMPI\=.*|MPI_WITH_PMPI\=\"yes\" \n
MPICH_INCLUDE_PROFLIB\=\"yes\" \n|' $i
done


for rep in $RPM_BUILD_ROOT/etc/mpich $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_sbindir} $RPM_BUILD_ROOT/usr/examples
do
  for file in $rep/*
  do
	if [ -f "$file" ];
	then
		perl -pi -e 's|%buildroot||g' "$file"
	fi
  done
done

#for i in $(ls $RPM_BUILD_ROOT/usr/bin/*); do
#perl -pi -e 's|MPI_WITH_PMPI\=\"yes\".*|MPI_WITH_PMPI\=yes \n MPICH_INCLUDE_PROFLIB\=yes|' $i
#done

HOSTNAME=`hostname`
perl -pi -e "s|$HOSTNAME||g" "$RPM_BUILD_ROOT%{_datadir}/mpich/machines.LINUX"

mkdir -p $RPM_BUILD_ROOT%{_docdir}
mkdir -p $RPM_BUILD_ROOT/%{mpihome}

install -m644 %{SOURCE1} $RPM_BUILD_DIR/%{name}-%{version}/rhosts

mkdir -p $RPM_BUILD_ROOT/usr/adm

find $RPM_BUILD_ROOT -name CVS -type d | xargs rm -rf

# A sample mpi program (hello world)
$RPM_BUILD_DIR/%{name}-%{version}/bin/mpicc -I$RPM_BUILD_ROOT/usr/include -L$RPM_BUILD_ROOT%_libdir %{SOURCE2} -o $RPM_BUILD_DIR/%{name}-%{version}/test_mpi.%{name}

cd $RPM_BUILD_ROOT/%{_libdir}
rm libpmpich.so*
ln -sf libmpich.so.1.0 libmpich.so
ln -sf libfmpich.so.1.0 libfmpich.so

#Cleaning uncessary files 
rm -f  $RPM_BUILD_ROOT%{_mandir}/mandesc*
rm -rf $RPM_BUILD_ROOT%{_libdir}/shared
rm -rf $RPM_BUILD_ROOT%{_datadir}/examples
rm -rf $RPM_BUILD_ROOT%{_datadir}/upshot
rm -rf $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%postun -n %{lib_name}
/sbin/ldconfig

%post -n %{lib_name}
/sbin/ldconfig

%files
%defattr(-,root,root,755)
%doc COPYRIGHT 
%doc test_mpi.mpich
%doc rhosts
%{_sbindir}/*
%{_bindir}/mpirun*
%{_bindir}/mpereconfig
%{_bindir}/mpereconfig.dat
%{_bindir}/mpereconfig.in
%{_bindir}/mpiman
%{_bindir}/mpireconfig
%{_bindir}/mpireconfig.dat
%{_bindir}/tarch
%{_bindir}/tdevice
%{_bindir}/serv_p4
%{_bindir}/clog2alog
%{_bindir}/clog2slog
%{_bindir}/clog_print
%{_bindir}/slog_print
%{_bindir}/logviewer
%config(noreplace) %{_sysconfdir}/mpich/*
%config(noreplace) %{_datadir}/mpich/*
%{_mandir}/man1/mpirun.1*
%{_mandir}/man1/mpiman.1*
%{_mandir}/man1/mpireconfig.1*
%{_mandir}/man1/tstmachines.1*
%{_mandir}/man1/chp4_servs.1*
%{_mandir}/man1/cleanipcs.1*
%{_mandir}/man1/MPI.1*
%{_mandir}/man1/Jumpshots.1*
/usr/adm

%files -n %{lib_name}
%defattr(-,root,root,755)
%{_libdir}/*.so.*

%files -n mpich-doc
%defattr(644,root,root,755)
%doc doc/* examples www  

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc COPYRIGHT
%{_mandir}/man3/*.3*
%{_mandir}/man4/*.4*
%dir %{_includedir}/mpi2c++
%{_includedir}/mpi2c++/*.h
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.o
%{_libdir}/*.so

%files -n mpicc
%defattr(-,root,root,755)
%doc COPYRIGHT
%{_bindir}/mpicc
%{_mandir}/man1/mpicc.1*

%files -n mpic++
%defattr(-,root,root,755)
%doc COPYRIGHT
%{_bindir}/mpiCC
%{_mandir}/man1/mpiCC.1*

%files -n mpif77
%defattr(-,root,root,755)
%doc COPYRIGHT
%{_bindir}/mpif77
%{_bindir}/mpif90
%{_mandir}/man1/mpif77.1*
%{_mandir}/man1/mpif90.1*
