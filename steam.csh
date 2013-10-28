# Disable Ubuntu 32 bit runtime
if ( -x /usr/bin/steam ) then
  setenv STEAM_RUNTIME "0"
endif

