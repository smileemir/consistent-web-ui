# Product notes

How Tidewell behaves. Keep UI copy consistent with these notes.

## Workspace settings

- **Workspace name**: shown in the app header and on invoices.
- **Time zone**: used for reports, the weekly digest and where "today" starts. Changing it does not move existing time entries.
- **Data retention (days)**: time entries older than this are archived, not deleted. Archived entries drop out of reports; an admin can restore them within 30 days. The minimum is 90 days.
- **Weekly digest**: a summary email every Monday at 08:00 in the workspace time zone, sent to members who have notifications turned on.
- **Require two-factor authentication**: every member must set up an authenticator app at their next sign-in. Until they do, they cannot open the workspace.

## API

- **API key**: gives full read and write access to the workspace's data through the API.
- **Regenerate key**: creates a new key and stops the old one immediately, so existing integrations stop working until they get the new key.

## Deleting a workspace

- **Delete workspace** schedules the deletion of all projects and time entries. The owner gets an email and can cancel within 7 days. After that the deletion is permanent.
