# Stem-IAA Portal

The Stem-IAA Portal was created to provide a way for students, instructors, and mentors to interact in various ways over the duration of a course. It is meant to supplement an Education Management System, rather than replace it. Importantly, however, mentors of the course do not have access to the EMS, and thus features are provided in the portal to counteract this.

The following topics are discussed in this documentation:

- Portal setup
- Portal usage guide
- Flask/static hosting information
- Virtual machine information
- Supplementary scripts


## Portal Setup

Before running, create a new file `config.json` in the root directory for the project. In this file, provide the following information:

- "secret": A complex random value sent to the flask app for cryptography.
- "SQLALCHEMY_DATABASE_URI": The URI pointing to the database to use for the portal. Example: `sqlite:///worm.db`
- "azure": A new dictionary with the following values found in the azure account:
    - "client_id"
    - "secret"
    - "tenant"
    - "subscription_id"

## Portal Usage

Pre-login, the portal serves a single static page describing the content of the course. In future courses, this page and simply be swapped for a page describing a different course. The same login button should be kept, however, which allows students/mentors/instructors to login to their accounts. The initial administrator account can be initialized via the [create admin script](util/create_admin.py). Subsequent accounts can be created on the /register page. This is intended to be performed ahead of time by an administrator; there is no way to create an account without an administrator account, and as such students can not create their own accounts.

After logging in, the user is taken to their profile page. The profile is visible to all other users in their cohort. Visible elements on a profile can be changed by clicking the `Edit` button at the top right, changing the content, and then clicking `Save`. In edit mode, the profile picture can be changed by clicking on it. The `Content` section is intended to be used by students to demonstrate the projects they are creating from the course. However, the content page exists on mentor and instructor accounts as well, in case there are other reasons to use it.

Information set during account creation can also be changed via the username dropdown -> Account option. The settings available to set will change depending on the type of account (student/mentor/instructor). For example, students don't have permission to change their username after it's been assigned. If a locked setting needs to be changed, an administrator can navigate to the student/mentor's profile and click the `Settings` button for the profile at the top right.
 