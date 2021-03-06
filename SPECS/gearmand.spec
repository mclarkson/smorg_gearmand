# Disable compressing/stripping
%define __os_install_post %{nil}
# boost differences between el5 and el6
%define boost boost-program-options
%if "%{?dist}" == ".el5"
%define boost boost141-program-options
%endif

Summary: Gearman Server and C Library
Name: smorg-gearmand
Version: 0.33
Release: 1
License: BSD
Group: System Environment/Libraries
BuildRequires: gcc-c++
URL: http://launchpad.net/gearmand
Requires: sqlite, libevent >= 1.4, %boost >=  1.39

Packager: Brian Aker <brian@tangent.org>

#Source: http://launchpad.net/gearmand/trunk/%{version}/+download/gearmand-%{version}.tar.gz
Source: smorg-gearmand-0.33.tar.gz
#Source1: gearmand.init
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Gearman provides a generic framework to farm out work to other machines, dispatching function calls to machines that are better suited to do work, to do work in parallel, to load balance processing, or to call functions between languages.

This package provides the client utilities.

%package server
Summary: Gearmand Server
Group: Applications/Databases
Requires: sqlite, libevent >= 1.4, %boost >=  1.39

%description server
Gearman provides a generic framework to farm out work to other machines, dispatching function calls to machines that are better suited to do work, to do work in parallel, to load balance processing, or to call functions between languages.

This package provides the Gearmand Server.

%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, 
you will need to install %{name}-devel.

%prep
%setup -q

%configure --disable-libpq --disable-libtokyocabinet --disable-libdrizzle --disable-libmemcached


%build
%{__make} %{_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install  DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""
mkdir -p $RPM_BUILD_ROOT/
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT/var/log/gearmand
mkdir -p $RPM_BUILD_ROOT/var/run/gearmand
mkdir -p $RPM_BUILD_ROOT/var/lib/gearmand
install -m 755 $RPM_BUILD_DIR/%buildsubdir/support/gearmand.init $RPM_BUILD_ROOT/etc/rc.d/init.d/gearmand

%clean
%{__rm} -rf %{buildroot}

%pre server
if ! /usr/bin/id -g gearmand &>/dev/null; then
    /usr/sbin/groupadd -r gearmand
fi
if ! /usr/bin/id gearmand &>/dev/null; then
    /usr/sbin/useradd -M -r -g gearmand -d /var/lib/gearmand -s /bin/false \
	-c "Gearman Server" gearmand > /dev/null 2>&1
fi

%post server
if test $1 = 1
then
  /sbin/chkconfig --add gearmand
fi

%preun server
if test $1 = 0
then
  /sbin/chkconfig --del gearmand
fi

%postun server
if test $1 -ge 1
then
  /sbin/service gearmand condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README HACKING THANKS
%{_bindir}/gearadmin
%{_bindir}/gearman
%{_libdir}/libgearman.la
%{_libdir}/libgearman.so.6
%{_libdir}/libgearman.so.6.0.0
%{_mandir}/man1/gearadmin.1
%{_mandir}/man1/gearman.1

%files server
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README HACKING THANKS
%{_mandir}/man8/gearmand.8
%{_sbindir}/gearmand
/etc/rc.d/init.d/gearmand
%attr(0755,gearmand,gearmand) %dir /var/log/gearmand
%attr(0755,gearmand,gearmand) %dir /var/run/gearmand
%attr(0755,gearmand,gearmand) %dir /var/lib/gearmand

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README HACKING THANKS
#%{_libdir}/libgearman.a
%{_includedir}/libgearman/gearman.h
%{_includedir}/libgearman-1.0/actions.h
%{_includedir}/libgearman-1.0/aggregator.h
%{_includedir}/libgearman-1.0/allocator.h
%{_includedir}/libgearman-1.0/argument.h
%{_includedir}/libgearman-1.0/client.h
%{_includedir}/libgearman-1.0/client_callbacks.h
%{_includedir}/libgearman-1.0/configure.h
%{_includedir}/libgearman-1.0/connection.h
%{_includedir}/libgearman-1.0/constants.h
%{_includedir}/libgearman-1.0/core.h
%{_includedir}/libgearman-1.0/execute.h
%{_includedir}/libgearman-1.0/function.h
%{_includedir}/libgearman-1.0/gearman.h
%{_includedir}/libgearman-1.0/job.h
%{_includedir}/libgearman-1.0/job_handle.h
%{_includedir}/libgearman-1.0/packet.h
%{_includedir}/libgearman-1.0/parse.h
%{_includedir}/libgearman-1.0/priority.h
%{_includedir}/libgearman-1.0/protocol.h
%{_includedir}/libgearman-1.0/result.h
%{_includedir}/libgearman-1.0/return.h
%{_includedir}/libgearman-1.0/strerror.h
%{_includedir}/libgearman-1.0/string.h
%{_includedir}/libgearman-1.0/task.h
%{_includedir}/libgearman-1.0/task_attr.h
%{_includedir}/libgearman-1.0/universal.h
%{_includedir}/libgearman-1.0/util.h
%{_includedir}/libgearman-1.0/version.h
%{_includedir}/libgearman-1.0/visibility.h
%{_includedir}/libgearman-1.0/worker.h
%{_includedir}/libgearman-1.0/kill.h
%{_includedir}/libgearman-1.0/limits.h
%{_includedir}/libgearman-1.0/ostream.hpp
%{_includedir}/libgearman-1.0/signal.h
%{_libdir}/pkgconfig/gearmand.pc
%{_libdir}/libgearman.so
%{_mandir}/man3/gearman_actions_t.3
%{_mandir}/man3/gearman_allocator_t.3
%{_mandir}/man3/gearman_argument_make.3
%{_mandir}/man3/gearman_argument_t.3
%{_mandir}/man3/gearman_bugreport.3
%{_mandir}/man3/gearman_client_add_options.3
%{_mandir}/man3/gearman_client_add_server.3
%{_mandir}/man3/gearman_client_add_servers.3
%{_mandir}/man3/gearman_client_add_task.3
%{_mandir}/man3/gearman_client_add_task_background.3
%{_mandir}/man3/gearman_client_add_task_high.3
%{_mandir}/man3/gearman_client_add_task_high_background.3
%{_mandir}/man3/gearman_client_add_task_low.3
%{_mandir}/man3/gearman_client_add_task_low_background.3
%{_mandir}/man3/gearman_client_add_task_status.3
%{_mandir}/man3/gearman_client_clear_fn.3
%{_mandir}/man3/gearman_client_clone.3
%{_mandir}/man3/gearman_client_context.3
%{_mandir}/man3/gearman_client_create.3
%{_mandir}/man3/gearman_client_do.3
%{_mandir}/man3/gearman_client_do_background.3
%{_mandir}/man3/gearman_client_do_high.3
%{_mandir}/man3/gearman_client_do_high_background.3
%{_mandir}/man3/gearman_client_do_job_handle.3
%{_mandir}/man3/gearman_client_do_low.3
%{_mandir}/man3/gearman_client_do_low_background.3
%{_mandir}/man3/gearman_client_do_status.3
%{_mandir}/man3/gearman_client_echo.3
%{_mandir}/man3/gearman_client_errno.3
%{_mandir}/man3/gearman_client_error.3
%{_mandir}/man3/gearman_client_free.3
%{_mandir}/man3/gearman_client_has_option.3
%{_mandir}/man3/gearman_client_job_status.3
%{_mandir}/man3/gearman_client_options.3
%{_mandir}/man3/gearman_client_options_t.3
%{_mandir}/man3/gearman_client_remove_options.3
%{_mandir}/man3/gearman_client_remove_servers.3
%{_mandir}/man3/gearman_client_run_tasks.3
%{_mandir}/man3/gearman_client_set_complete_fn.3
%{_mandir}/man3/gearman_client_set_context.3
%{_mandir}/man3/gearman_client_set_created_fn.3
%{_mandir}/man3/gearman_client_set_data_fn.3
%{_mandir}/man3/gearman_client_set_exception_fn.3
%{_mandir}/man3/gearman_client_set_fail_fn.3
%{_mandir}/man3/gearman_client_set_log_fn.3
%{_mandir}/man3/gearman_client_set_memory_allocators.3
%{_mandir}/man3/gearman_client_set_namespace.3
%{_mandir}/man3/gearman_client_set_options.3
%{_mandir}/man3/gearman_client_set_status_fn.3
%{_mandir}/man3/gearman_client_set_task_context_free_fn.3
%{_mandir}/man3/gearman_client_set_timeout.3
%{_mandir}/man3/gearman_client_set_warning_fn.3
%{_mandir}/man3/gearman_client_set_workload_fn.3
%{_mandir}/man3/gearman_client_set_workload_free_fn.3
%{_mandir}/man3/gearman_client_set_workload_malloc_fn.3
%{_mandir}/man3/gearman_client_st.3
%{_mandir}/man3/gearman_client_task_free_all.3
%{_mandir}/man3/gearman_client_timeout.3
%{_mandir}/man3/gearman_client_wait.3
%{_mandir}/man3/gearman_continue.3
%{_mandir}/man3/gearman_execute.3
%{_mandir}/man3/gearman_failed.3
%{_mandir}/man3/gearman_job_free.3
%{_mandir}/man3/gearman_job_free_all.3
%{_mandir}/man3/gearman_job_function_name.3
%{_mandir}/man3/gearman_job_handle.3
%{_mandir}/man3/gearman_job_handle_t.3
%{_mandir}/man3/gearman_job_send_complete.3
%{_mandir}/man3/gearman_job_send_data.3
%{_mandir}/man3/gearman_job_send_exception.3
%{_mandir}/man3/gearman_job_send_fail.3
%{_mandir}/man3/gearman_job_send_status.3
%{_mandir}/man3/gearman_job_send_warning.3
%{_mandir}/man3/gearman_job_st.3
%{_mandir}/man3/gearman_job_take_workload.3
%{_mandir}/man3/gearman_job_unique.3
%{_mandir}/man3/gearman_job_workload.3
%{_mandir}/man3/gearman_job_workload_size.3
%{_mandir}/man3/gearman_log_fn.3
%{_mandir}/man3/gearman_parse_servers.3
%{_mandir}/man3/gearman_result_boolean.3
%{_mandir}/man3/gearman_result_integer.3
%{_mandir}/man3/gearman_result_is_null.3
%{_mandir}/man3/gearman_result_size.3
%{_mandir}/man3/gearman_result_store_integer.3
%{_mandir}/man3/gearman_result_store_string.3
%{_mandir}/man3/gearman_result_store_value.3
%{_mandir}/man3/gearman_result_string.3
%{_mandir}/man3/gearman_return_t.3
%{_mandir}/man3/gearman_strerror.3
%{_mandir}/man3/gearman_string_t.3
%{_mandir}/man3/gearman_success.3
%{_mandir}/man3/gearman_task_attr_init.3
%{_mandir}/man3/gearman_task_attr_init_background.3
%{_mandir}/man3/gearman_task_attr_init_epoch.3
%{_mandir}/man3/gearman_task_attr_t.3
%{_mandir}/man3/gearman_task_context.3
%{_mandir}/man3/gearman_task_data.3
%{_mandir}/man3/gearman_task_data_size.3
%{_mandir}/man3/gearman_task_denominator.3
%{_mandir}/man3/gearman_task_error.3
%{_mandir}/man3/gearman_task_free.3
%{_mandir}/man3/gearman_task_function_name.3
%{_mandir}/man3/gearman_task_give_workload.3
%{_mandir}/man3/gearman_task_is_known.3
%{_mandir}/man3/gearman_task_is_running.3
%{_mandir}/man3/gearman_task_job_handle.3
%{_mandir}/man3/gearman_task_numerator.3
%{_mandir}/man3/gearman_task_recv_data.3
%{_mandir}/man3/gearman_task_return.3
%{_mandir}/man3/gearman_task_send_workload.3
%{_mandir}/man3/gearman_task_set_context.3
%{_mandir}/man3/gearman_task_st.3
%{_mandir}/man3/gearman_task_take_data.3
%{_mandir}/man3/gearman_task_unique.3
%{_mandir}/man3/gearman_verbose_name.3
%{_mandir}/man3/gearman_verbose_t.3
%{_mandir}/man3/gearman_version.3
%{_mandir}/man3/gearman_worker_add_function.3
%{_mandir}/man3/gearman_worker_add_options.3
%{_mandir}/man3/gearman_worker_add_server.3
%{_mandir}/man3/gearman_worker_add_servers.3
%{_mandir}/man3/gearman_worker_clone.3
%{_mandir}/man3/gearman_worker_context.3
%{_mandir}/man3/gearman_worker_create.3
%{_mandir}/man3/gearman_worker_define_function.3
%{_mandir}/man3/gearman_worker_echo.3
%{_mandir}/man3/gearman_worker_errno.3
%{_mandir}/man3/gearman_worker_error.3
%{_mandir}/man3/gearman_worker_free.3
%{_mandir}/man3/gearman_worker_function_exist.3
%{_mandir}/man3/gearman_worker_grab_job.3
%{_mandir}/man3/gearman_worker_options.3
%{_mandir}/man3/gearman_worker_register.3
%{_mandir}/man3/gearman_worker_remove_options.3
%{_mandir}/man3/gearman_worker_remove_servers.3
%{_mandir}/man3/gearman_worker_set_context.3
%{_mandir}/man3/gearman_worker_set_log_fn.3
%{_mandir}/man3/gearman_worker_set_memory_allocators.3
%{_mandir}/man3/gearman_worker_set_namespace.3
%{_mandir}/man3/gearman_worker_set_options.3
%{_mandir}/man3/gearman_worker_set_timeout.3
%{_mandir}/man3/gearman_worker_set_workload_free_fn.3
%{_mandir}/man3/gearman_worker_set_workload_malloc_fn.3
%{_mandir}/man3/gearman_worker_st.3
%{_mandir}/man3/gearman_worker_timeout.3
%{_mandir}/man3/gearman_worker_unregister.3
%{_mandir}/man3/gearman_worker_unregister_all.3
%{_mandir}/man3/gearman_worker_wait.3
%{_mandir}/man3/gearman_worker_work.3
%{_mandir}/man3/libgearman.3


%changelog
* Wed Jan 7 2009 Brian Aker <brian@tangent.org> - 0.1-1
- Initial package
