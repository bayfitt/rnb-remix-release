# RNB Remix AI Creator CLI privacy

This is a personal YouTube creation and channel-management installation. The public repository contains workflow instructions and CLI helper code; it does not host an account-collection service.

Google authorization lets the configured local tools upload and update videos, manage caption tracks and thumbnails, read comments, and read channel analytics. The OAuth scopes cover broader YouTube management capabilities, but the release workflow performs only actions requested or authorized by the channel owner. Analytics access is read-only.

OAuth client credentials and refresh tokens are stored in private files on the account owner’s computer. They are excluded from this public repository. Native YouTube CLI requests go to Google APIs. Channel metadata, comments and analytics may be reviewed by the owner’s chosen AI assistant under that assistant service’s privacy terms. The workflow does not sell Google user data or use it for advertising targeting.

Videos, titles, descriptions, artwork and caption tracks become public when the owner authorizes publication. Authorized sharing destinations receive the release links; private OAuth credentials and raw analytics are not included in those messages. Music and image generation use separately selected providers for their creative inputs; Google OAuth tokens are not sent to those providers.

Local project records, downloaded comments and analytics remain until the owner removes them. Access can be revoked at any time through [Google Account third-party connections](https://myaccount.google.com/connections); local token files can also be deleted to disconnect the tools. Revoking access does not itself remove previously published videos.

Questions about this repository can be opened as [GitHub issues](https://github.com/bayfitt/rnb-remix-release/issues). Do not post credentials or private channel data in an issue.
