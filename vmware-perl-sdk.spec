%global nextcloud_token T22XMg2RWEX68HE
%global vmware_sdk_version 6.5.0-4566394
%global vmware_pkg_verison %(v=%{vmware_sdk_version}; echo ${v//-/.})

Summary:        VMware vSphere Perl SDK
Name:           vmware-perl-sdk
Version:        %{vmware_pkg_verison}
Release:        1%{?dist}
License:        VMware(r) vSphere Software Development Kit License
Url:            https://my.vmware.com/de/web/vmware/details?downloadGroup=VS-PERL-SDK65&productId=614
#Group:          System/Monitoring
Source:         https://nextcloud.netways.de/index.php/s/%{nextcloud_token}/download?path=%2F&files=VMware-vSphere-Perl-SDK-%{vmware_sdk_version}.%{_target_cpu}.tar.gz#/VMware-vSphere-Perl-SDK-%{vmware_sdk_version}.%{_target_cpu}.tar.gz

Patch0:         vmware-perl-sdk-destdir.patch
Patch1:         vmware-perl-sdk-makemaker-exclude.patch
Patch2:         vmware-perl-sdk-ssl-verify.patch

%define debug_package %{nil}

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)

Requires:       perl(Archive::Zip)
Requires:       perl(Crypt::SSLeay)
Requires:       perl(LWP)
Requires:       perl(SOAP::Lite)
Requires:       perl(XML::LibXML)

AutoProv: no
%{?perl_default_filter}
%{?filter_setup:
%filter_provides_in /usr/lib/vmware-viperl
%filter_provides_in /usr/share/doc/vmware-viperl
%filter_requires_in /usr/lib/vmware-viperl
%filter_requires_in /usr/share/doc/vmware-viperl
%filter_from_provides /perl(/d
%filter_from_requires /perl(VMware/d; /perl(WSMan/d
# TODO: temporary - needs manual install for now
%filter_from_requires /perl(UUID)/d
%filter_setup
}

%description
VMware vSphere Perl SDK

%prep
%setup -q -n vmware-vsphere-cli-distrib
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
export PERL_MM_USE_DEFAULT=1
perl Makefile.PL INSTALLDIRS=vendor

%install
make install DESTDIR="%{buildroot}"

rm -f %{buildroot}%{_libdir}/perl5/perllocal.pod
rm -f %{buildroot}%{_libdir}/perl5/vendor_perl/auto/VIPerlToolkit/.packlist

%pre
uninstaller=/usr/bin/vmware-uninstall-vSphere-CLI.pl

if [ -f "$uninstaller" ]; then
  (
    echo "The original uninstaller $uninstaller is present!"
    echo
    echo "Please make sure to remove an old installation by using the uninstaller,"
    echo "or at least remove the script from the system"
  ) >&2
  exit 1
fi

%files
%defattr(-,root,root,-)
%doc doc/EULA
/usr/share/perl5/vendor_perl/VMware
/usr/share/perl5/vendor_perl/WSMan

/usr/lib/vmware-viperl

/usr/share/doc/vmware-viperl
/usr/share/man/man3

%changelog
* Tue Nov 20 2018 Markus Frosch <markus.frosch@icinga.com> 6.5.0-4566394-1
- Initial RPM package
