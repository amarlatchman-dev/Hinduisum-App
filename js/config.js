/* Dharma Path: settings for services outside the app.
   googleClientId: the OAuth client ID that lets people sync through their own Google Drive. It is
   not a secret (it is visible to anyone who opens the app); see docs/SYNC_SETUP.md. Leave it empty
   and the Sync page explains that sync isn't set up, while backup and restore still work. */
window.DP_CONFIG = {
  googleClientId: ""
};
