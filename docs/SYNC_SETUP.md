# Turning on sync between devices

Dharma Path syncs through each person's **own Google Drive**. The app keeps its data in a hidden
app folder in their Drive, which only Dharma Path can open. There is no Dharma Path server, nothing
to pay for, and you never see anyone's data.

To switch it on, Google needs to know about the app. This takes about ten minutes, once.

## 1. Create a Google Cloud project

1. Go to <https://console.cloud.google.com/> and sign in with the Google account that will own the app.
2. Click the project picker at the top, then **New project**. Name it `Dharma Path` and create it.

## 2. Turn on the Google Drive API

1. In the menu, choose **APIs & Services → Library**.
2. Search for **Google Drive API**, open it and click **Enable**.

## 3. Set up the sign-in screen

1. Choose **APIs & Services → OAuth consent screen** (in newer consoles: **Google Auth Platform → Branding**).
2. User type: **External**.
3. App name: `Dharma Path`. Add a support email and the developer contact email.
4. App home page: `https://amarlatchman-dev.github.io/Hinduisum-App/`.
5. Under **Data access** (or **Scopes**), add the scope
   `https://www.googleapis.com/auth/drive.appdata` ("See, create, and delete its own configuration
   data in your Google Drive"). This narrow scope lets the app see only its own hidden folder, never
   anyone's files.
6. Under **Audience**, click **Publish app** so that anyone can sign in, not just test users.

## 4. Create the client ID

1. Choose **APIs & Services → Credentials → Create credentials → OAuth client ID**.
2. Application type: **Web application**. Name: `Dharma Path web`.
3. **Authorised JavaScript origins**: add `https://amarlatchman-dev.github.io`.
   (For testing on your own computer you can also add `http://localhost:8123`.)
4. No redirect URIs are needed. Click **Create**.
5. Copy the **Client ID**. It looks like `123456789012-abc…xyz.apps.googleusercontent.com`.

## 5. Put the client ID in the app

Open `js/config.js` and paste the client ID between the quotes:

```js
window.DP_CONFIG = {
  googleClientId: "123456789012-abc…xyz.apps.googleusercontent.com"
};
```

Commit the change. The client ID is **not a secret**: it is meant to be visible in the app, and
Google only accepts it from the origins listed in step 4. (Never put a *client secret* in the app;
sync doesn't need one.)

Once the site updates, the **Sync** page (Practice → Sync between devices) offers "Sign in with
Google and sync".

## How it behaves

- Each device signs in once per session; Google's sign-in lasts about an hour, during which changes
  sync by themselves. After that, "Sync now" asks to sign in again (usually one tap).
- When only one device has changed something since the last sync, its version wins, so deletions
  carry across. When both have, the two are merged.
- Recordings stay on the device where they were made (they are large); backup and restore moves them.
- People can remove the app's data at any time from Google Drive → Settings → Manage apps.
