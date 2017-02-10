# Improved interactions between the Steam runtime and host distribution
# libraries, which should let Steam work out of the box with open-source
# graphics drivers on modern distributions. If using an older distribution or
# running into problems, set variable at 0 to revert to the previous behavior.
# setenv STEAM_RUNTIME_PREFER_HOST_LIBRARIES 0

# Unify close-to-tray behavior with other platforms. If using a distribution
# that doesn't have proper compatible tray support set variable at 0.
setenv STEAM_FRAME_FORCE_CLOSE 1
