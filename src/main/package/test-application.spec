%define _htmldir /srv/www/htdocs/
%define apacheconf %{_sysconfdir}/apache2/conf.d
%define _prefix @applicationPrefix@

Name: @projectName@
Summary: @applicationName@
Version: @applicationVersion@
Release: @applicationRelease@
License: Commercial
Group: Productivity/Scientific/Astronomy
Packager: @vendorPackager@
Vendor: @vendorName@
URL: @vendorUrl@
Requires: xdg-utils
Provides: %{name}
Prefix: %{_prefix}
BuildArch: x86_64

Autoprov: 0
Autoreq: 0
%if "xglibc, libX11-6, libXau6, libXext6, libXi6, libXrender1, libXtst6, libasound2, libxcb1, libz1" != x || "x" != x
Requires: glibc, libX11-6, libXau6, libXext6, libXi6, libXrender1, libXtst6, libasound2, libxcb1, libz1
%endif

#avoid ARCH subfolder
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

#comment line below to enable effective jar compression
#it could easily get your package size from 40 to 15Mb but
#build time will substantially increase and it may require unpack200/system java to install
%define __jar_repack %{nil}

%description
@projectDescription@

%prep

%build

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_prefix}/%{name}
cp -r %{_sourcedir}%{_prefix}/%{name}/* %{buildroot}%{_prefix}/%{name}
%if "x" != x
  %define license_install_file %{_defaultlicensedir}/%{name}-%{version}/%{basename:}
  install -d -m 755 %{buildroot}%{dirname:%{license_install_file}}
  install -m 644  %{buildroot}%{license_install_file}
%endif

%files
# If installation directory for the application is /a/b/c, we want only root
# component of the path (/a) in the spec file to make sure all subdirectories
# are owned by the package.
%(echo %{_prefix}/%{name} | sed -e "s|\(^/[^/]\{1,\}\).*$|\1|")

%post
#-------------
# Add menu items and symlinks on install.
ln -sf %{_prefix}/%{name}/bin/%{name} /usr/bin/%{name}

# Add icons to the system icons
XDG_ICON_RESOURCE="`which xdg-icon-resource 2> /dev/null`"
if [ ! -x "$XDG_ICON_RESOURCE" ]; then
  echo "Error: Could not find xdg-icon-resource" >&2
  exit 1
fi
"$XDG_ICON_RESOURCE" install --novendor --size 128 %{_prefix}/%{name}/lib/%{name}.png %{name}

# Add an entry to the system menu
XDG_DESKTOP_MENU="`which xdg-desktop-menu 2> /dev/null`"
if [ ! -x "$XDG_DESKTOP_MENU" ]; then
  echo "Error: Could not find xdg-desktop-menu" >&2
  exit 1
fi
"$XDG_DESKTOP_MENU" install --novendor %{_prefix}/%{name}/bin/%{name}.desktop || echo "xdg-desktop-menu failed"

%preun
#-------------
# Remove menu items and symlinks on uninstall. When upgrading,
# old_pkg's %preun runs after new_pkg's %post.
if [ "$1" = "0" ]; then
  rm -f /usr/bin/%{name}

  # Remove icons from the system icons
  XDG_ICON_RESOURCE="`which xdg-icon-resource 2> /dev/null`"
  if [ ! -x "$XDG_ICON_RESOURCE" ]; then
    echo "Error: Could not find xdg-icon-resource" >&2
    exit 1
  fi
  "$XDG_ICON_RESOURCE" uninstall --size 128 %{name}

  # Remove the entry from the system menu
  XDG_DESKTOP_MENU="`which xdg-desktop-menu 2> /dev/null`"
  if [ ! -x "$XDG_DESKTOP_MENU" ]; then
    echo "Error: Could not find xdg-desktop-menu" >&2
    exit 1
  fi
  "$XDG_DESKTOP_MENU" uninstall %{_prefix}/%{name}/bin/%{name}.desktop
fi

%clean
