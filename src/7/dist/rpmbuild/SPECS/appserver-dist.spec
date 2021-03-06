%define         _unpackaged_files_terminate_build 0
%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

Name:       ${build.name.prefix}dist
Version:    ${appserver.src.semver}
Release:    ${build.number}${appserver.src.suffix}%{?dist}
Summary:    appserver.io provides a multithreaded application server for PHP.
Group:      System Environment/Base
License:    OSL 3.0
Vendor:     Bernhard Wick bw@appserver.io
URL:        http://appserver.io
requires:   appserver-runtime
Provides:   appserver-dist

%description
%{summary}


%prep


%build


%clean

%files
/opt/appserver/*
/lib/systemd/system/*
/usr/sbin/*

%post
if [ "$1" = "1" ]
then
  # Perform tasks after the initial installation

  # Setup appserver by calling server.php with -s install to trigger install mode setup
  /opt/appserver/server.php -s install

  # Set needed files as accessable for the configured user
  chmod 755 /usr/sbin/appserverctl

  # Make the link to our system systemd file
  ln -sf /lib/systemd/system/appserver.service /etc/systemd/system/appserver.service
  ln -sf /lib/systemd/system/appserver-watcher.service /etc/systemd/system/appserver-watcher.service
  ln -sf /lib/systemd/system/appserver-php5-fpm.service /etc/systemd/system/appserver-php5-fpm.service

  # Start the appserver + watcher + fpm
  systemctl start appserver.service
  systemctl start appserver-watcher.service
  systemctl start appserver-php5-fpm.service
fi

# Reload shared library list
ldconfig

# Reload the systemd daemon
  systemctl daemon-reload


%preun
if [ "$1" = "0" ]
then
  # Perform tasks before un-installation

  # Stop the appserver + watcher + fpm
  systemctl stop appserver.service
  systemctl stop appserver-watcher.service
  systemctl stop appserver-php5-fpm.service
fi


%postun
if [ "$1" = "1" ]
then
  # Perform tasks to do after the upgrade

  # Conditionally restart the appserver + watcher + fpm
  systemctl status appserver > /dev/null 2>&1;
  if [ $? -eq 0 ]
  then
    systemctl restart appserver.service
  fi

  systemctl status appserver-watcher > /dev/null 2>&1;
  if [ $? -eq 0 ]
  then
    systemctl restart appserver-watcher.service
  fi

  systemctl status appserver-php5-fpm > /dev/null 2>&1;
  if [ $? -eq 0 ]
  then
    systemctl restart appserver-php5-fpm.service
  fi
fi

# Reload shared library list
ldconfig
