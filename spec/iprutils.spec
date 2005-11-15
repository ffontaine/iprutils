Summary: Utilities for the IBM Power Linux RAID adapters
Name: iprutils
Version: 2.0.15.6
Release: 1
License: CPL
Group: System Environment/Base
Vendor: IBM
URL: http://sourceforge.net/projects/iprdd/
Source0: iprutils-%{version}-src.tgz
BuildRoot: %{_tmppath}/%{name}-root

%description
Provides a suite of utilities to manage and configure SCSI devices
supported by the ipr SCSI storage device driver.

%prep
%setup -q -n %{name}

%build
make

%install
make INSTALL_MOD_PATH=$RPM_BUILD_ROOT install
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/init.d
install -m 755 init.d/iprinit $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/iprinit
install -m 755 init.d/iprdump $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/iprdump
install -m 755 init.d/iprupdate $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/iprupdate

%ifarch ppc ppc64
%post
/usr/lib/lsb/install_initd %{_sysconfdir}/init.d/iprinit
/usr/lib/lsb/install_initd %{_sysconfdir}/init.d/iprdump
/usr/lib/lsb/install_initd %{_sysconfdir}/init.d/iprupdate
%endif

%ifarch ppc ppc64
%preun
if [ $1 = 0 ]; then
	%{_sysconfdir}/init.d/iprdump stop  > /dev/null 2>&1
	%{_sysconfdir}/init.d/iprupdate stop  > /dev/null 2>&1
	%{_sysconfdir}/init.d/iprinit stop  > /dev/null 2>&1
	/usr/lib/lsb/remove_initd %{_sysconfdir}/init.d/iprdump
	/usr/lib/lsb/remove_initd %{_sysconfdir}/init.d/iprupdate
	/usr/lib/lsb/remove_initd %{_sysconfdir}/init.d/iprinit
fi
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README LICENSE
/sbin/*
%{_mandir}/man*/*
%{_sysconfdir}/init.d/*

%changelog
* Tue Nov 15 2005 Brian King <brking@us.ibm.com> 2.0.15.6
- Fix concurrent maintenance with disk drawers reporting
  multiple SES devices on the same SCSI bus.
* Mon Oct 17 2005 Brian King <brking@us.ibm.com> 2.0.15.5
- Don't show enclosures in list of devices to remove in
  concurrent remove screens of iprconfig.
* Thu Oct 13 2005 Brian King <brking@us.ibm.com>
- Fix concurrent disk remove function in iprconfig for
  certain disk enclosures.
* Fri Oct 7 2005 Anton Blanchard <anton@samba.org>
- Fix string length calculation in ipr_get_hotplug_dir
* Wed Aug 17 2005 Brian King <brking@us.ibm.com> 2.0.15.4
- Fix a couple of uninitialized variable compile errors
* Wed Jul 27 2005 Brian King <brking@us.ibm.com> 2.0.15.3
- Fix: iprconfig: IOA microcode update would leave AF DASD
  (disks that are in disk arrays) in a state where they were
  no longer tagged queueing. Fix iprconfig to run iprinit on the
  adapter after a microcode download to ensure all attached devices
  are properly setup after a microcode download.
- Fix iprinit: If an IOA was reset for some reason at runtime,
  this would cause AF DASD devices to get tagged queueing turned
  off and it would never get turned back on. Change iprinit to
  detect this and turn tagged queueing back on if this happens.
- Changing the queue depth for a disk array was broken. Fix iprinit
  to properly restore the queue depth from the ipr configuration file.
- Fix iprconfig to handle disk format failures better
- Fix potential iprutils segfaults when iterating over disk arrays
* Sat Jul 23 2005 Brian King <brking@us.ibm.com> 2.0.15.2
- Fix: iprconfig: Concurrent remove/add of disks would display
  the same slot multiple times on some hardware due to SES devices
  returning bogus data. Work around this by only not showing duplicate
  slots.
* Fri Jul 22 2005 Brian King <brking@us.ibm.com> 2.0.15.2
- Fix: iprconfig: including a disk to a RAID 5 array when multiple
  RAID 5 arrays were attached would sometimes cause the disk
  to get included into the wrong array.
* Wed Jun 1 2005 Brian King <brking@us.ibm.com> 2.0.15.1
- Fix iprconfig Analyze Log options
* Wed May 18 2005 Brian King <brking@us.ibm.com> 2.0.15
- Clarify format options
- Setup mode page 0 for IBM drives to ensure command aging is
  enabled. This ensures commands are not starved on some drives.
- Fix so that iprdump properly names dump files once 100 dumps
  have been made.
- Make iprconfig handle failures of scsi disk formats better
- Fix iprconfig Set root kernel message log directory menu
- Properly display RAID level on all iprconfig screens
- Don't disable init.d daemons on an rpm -U
* Tue Apr 12 2005 Brian King <brking@us.ibm.com> 2.0.14.2
- Fixed bug preventing disk microcode update from working.
* Mon Apr 4 2005 Brian King <brking@us.ibm.com>
- Add ability to force RAID consistency check
* Mon Mar 25 2005 Brian King <brking@us.ibm.com> 2.0.14.1
- Removed mention of primary/secondary adapters in some error
  screens since multi-initiator RAID is not supported and the
  messages will just cause confusion.
* Mon Mar 24 2005 Brian King <brking@us.ibm.com>
- iprconfig: During disk hotplug, wait for sd devices to show
  up. Fixes errors getting logged by iprconfig during hotplug.
* Mon Mar 23 2005 Brian King <brking@us.ibm.com>
- iprconfig: Fix cancel path on concurrent add/remove of disks
- Don't display current bus width and speed for SAS disks
* Mon Mar 21 2005 Brian King <brking@us.ibm.com>
- Fix scoping bug caught by gcc 4.0.
* Fri Mar 18 2005 Brian King <brking@us.ibm.com>
- Stop iprupdate from continually logging errors for adapters with
  backlevel adapter firmware.
* Mon Mar 7 2005 Brian King <brking@us.ibm.com> 2.0.14
- Add support for non-interactive array creation and deletion through
  iprconfig.
- Use kobject_uevent notifications instead of polling if the kernel
  supports it.
- Fix iprconfig to set the actual queue depth for advanced function disks
- Allow user to force tagged queuing on to drives that do not support
  QERR=1.
- Fix handling of medium format corrupt drives for drives
- iprconfig: Download microcode. Fix blank screen when displaying
  lots of microcode images.
- Fix iprinit to wait for scsi generic devices to show up in case we are
  racing with hotplug. Fixes the following error:
      0:255:0:0: Mode Sense failed. rc=1, SK: 5 ASC: 24 ASCQ: 0
- Add "known to be zeroed" tracking to iprconfig to drastically reduce the
  time required to create a RAID array when starting with 512 formatted disks
- Add ability to query multi-adapter status for dual initiator RAID configs
- Add ability to set "preferred primary" adapter when running dual initiator RAID configs
- Add iprconfig screen to display dual adapter status for dual initiator RAID configs
- Prevent RAID configuration from occurring on "secondary" adapter in dual initiator RAID configs
- Use /dev/sd for SG_IO instead of /dev/sg when possible
- Set QERR=3 rather than 1 for multi-initiator configurations
- Set TST=1 for multi-initiator configurations
- Allow Format device for JBOD function to work for JBOD adapters
- Fix handling of dead adapters in all of iprutils.
- Fix iprconfig RAID start bug for systems with multiple RAID adapters.
- Fix iprconfig RAID include bug for systems with multiple RAID adapters.
- Fix failing array add device due to race condition with iprinit.
* Tue Oct 5 2004 Brian King <brking@us.ibm.com> 2.0.13
- Improve iprupdate error logs to indicate where to download microcode from.
- Set default tcq queue depth for AS400 disks to 16.
- Don't log errors in iprdump if CONFIG_IPR_DUMP not enabled in the kernel
- Fix sysfs parsing to handle new sdev target kernel change
- Rescan JBOD devices following recovery format to make the device usable if
  it was originally in an unsupported sector size.
- Display correct adapter serial number in iprconfig.
- Support for microcode download to new adapters.
- Support for iSeries disk microcode update using microcode images from
  the pSeries microcode website.
* Fri Jun 11 2004 Brian King <brking@us.ibm.com> 2.0.12
- Fix bug preventing ucode download to iSeries disks from working
* Thu Jun 10 2004 Brian King <brking@us.ibm.com> 2.0.11
- Fix segmentation fault in _sg_ioctl that was causing a silent
  failure of microcode update to disks. The microcode update would
  fail, but no error would be logged. The seg fault was in a child
  process, so the parent process kept running.
* Thu May 23 2004 Brian King <brking@us.ibm.com> 2.0.10
- Don't let iprdbg sg ioctls be retried.
- Add --force flag to iprconfig to allow user to workaround buggy
  drive firmware.
- Don't initialize read/write protected disks
- Fix some reclaim cache bugs
- Don't setup Mode Page 0x0A if test unit ready fails
* Thu May 2 2004 Brian King <brking@us.ibm.com> 2.0.9
- Add --debug option to all utilities
- Make utilities behave better when ipr is not loaded
- Fix dependencies in init.d scripts
- Only enable init.d scripts on ppc
- Don't log an error if ipr is not loaded
* Mon Apr 28 2004 Brian King <brking@us.ibm.com> 2.0.8
- Fix to properly enable init.d scripts when the rpm is installed
- Fix memory leak in code download path
- Increase size of page 0 inquiry buffer so that extended vpd is displayed
- Decrease write buffer timeout to 2 minutes
* Wed Apr 16 2004 Brian King <brking@us.ibm.com> 2.0.7
- Load sg module in init.d scripts if not loaded
- Load sg module in iprconfig if not loaded
* Wed Apr 14 2004 Brian King <brking@us.ibm.com> 2.0.6
- Battery maintenance fixes.
- Fix to properly display failed status for pulled physical disks.
* Tue Apr 6 2004 Brian King <brking@us.ibm.com> 2.0.5
- Battery maintenance fixes.
- Fix init.d scripts to work properly with yast runlevel editor.
- Fix device details screen in iprconfig for Failed array members
- Allow formatting devices even if qerr cannot be disabled 
* Tue Mar 29 2004 Brian King <brking@us.ibm.com> 2.0.4
- Fixed some sysfs calls that changed their calling interfaces
* Tue Mar 17 2004 Brian King <brking@us.ibm.com> 2.0.2-3
- Fixed 
