# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	0.3
Summary:	Intel® Wireless WiFi Link 4965AGN and Intel® PRO/Wireless 3945ABG Network Connection
Name:		iwlwifi
Version:	1.1.17
Release:	%{_rel}
License:	mixed GPL v2 and BSD
Group:		Base/Kernel
Source0:	http://www.intellinuxwireless.org/iwlwifi/downloads/%{name}-%{version}.tgz
# Source0-md5:	8c0ab70d569ae92315813855137d065f
URL:		http://www.intellinuxwireless.org/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
#ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The iwlwifi project provides a driver which utilizes the new mac80211
subsystem for the Intel® Wireless WiFi Link 4965AGN and Intel®
PRO/Wireless 3945ABG Network Connection adapters.

In addition to using the new mac80211 subsystem, this project uses a
new microcode image which removes the need for the user space
regulatory daemon. This change should help to simplify installation,
development, and redistribution of this driver package.

%package -n kernel%{_alt_kernel}-net-iwl3945
Summary:	Intel® PRO/Wireless 3945ABG Network Connection
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires:	hotplug
Requires:	iwlwifi-3945-ucode
%{?with_dist_kerqnel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2

%description -n kernel%{_alt_kernel}-net-iwl3945
This package contains Linux kernel drivers for the Intel�
PRO/Wireles 3945ABG Network Connection.

%package -n kernel%{_alt_kernel}-net-iwl4965
Summary:	Intel® Wireless WiFi Link 4965AG
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires:	hotplug
Requires:	iwlwifi-4965-ucode
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2

%description -n kernel%{_alt_kernel}-net-iwl4965
This package contains Linux kernel drivers for the Intel® Wireless WiFi
Link 4965AGN.

%prep
%setup -q
sed -i -e 's#$(CONFIG_IWL3945)#m#g' -e 's#$(CONFIG_IWL4965)#m#g' origin/Makefile

%build
%build_kernel_modules -C origin -m iwl3945,iwl4965 

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m origin/iwl3945 -d drivers/net/wireless
%install_kernel_modules -m origin/iwl4965 -d drivers/net/wireless

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-iwl3945
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-iwl3945
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-net-iwl4965
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-iwl4965
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-net-iwl3945
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/drivers/net/wireless/iwl3945.ko*
#%{_sysconfdir}/modprobe.d/%{_kernel_ver}/iwl3945.conf

%files -n kernel%{_alt_kernel}-net-iwl4965
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/drivers/net/wireless/iwl4965.ko*
#%{_sysconfdir}/modprobe.d/%{_kernel_ver}/iwl4965.conf
