%global koofr_dir %{_libexecdir}/koofr
%global hash 0db1c5f
# those binaries does not have debuginfo
%global debug_package %{nil} 
# turn off stripping othewise koofr will not find some resources
%global __strip /bin/true

Name:    koofr
Version: 0
Release: 0.%{hash}%{?dist}.1
Summary: Hybrid storage cloud 

License: Proprietary
URL:     https://koofr.eu/
# Downloaded from https://app.koofr.net/dl/apps/linux64
Source0: koofr-%{hash}-linux-x86_64.tar.gz 
Source1: koofr.desktop
BuildArch: x86_64

BuildRequires:  desktop-file-utils

Requires: gtk-update-icon-cache
Requires: desktop-file-utils
# HAS_UDEV1
Requires: systemd-libs

%description
Koofr is a safe, private and simple cloud storage service, accessible through
web, mobile, and WebDav. View all your files in one place by easily
connecting to existing cloud accounts (Dropbox, Google Drive, Amazon, and
OneDrive), and transfer huge files to external clouds with no limit.

%prep
%setup -q -n koofr


%build

%install
mkdir -p %{buildroot}/%{koofr_dir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart/

cp -a * %{buildroot}/%{koofr_dir}
rm -rf %{buildroot}/%{koofr_dir}/{installer.sh,Install.desktop}
ln -sf %{koofr_dir}/storagegui %{buildroot}%{_bindir}/koofr

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}
ln -sf ../../%{_datadir}/applications/koofr.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/

# waive RPATH error
# ERROR   0004: file '/usr/libexec/koofr/storagechrome' contains an insecure rpath '.' in [.:$ORIGIN]
# ERROR   0008: file '/usr/libexec/koofr/storagechrome' contains the $ORIGIN rpath specifier at the w
export QA_RPATHS=$[ 0x0004|0x0008 ]

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

	
%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

	
%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%{_bindir}/koofr
%{koofr_dir}

%config(noreplace) %{_sysconfdir}/xdg/autostart/*
%{_datadir}/applications


%changelog


