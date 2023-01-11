# Gitlab Group Projects Backup

Docker image that uses Python to backup all projects in a Gitlab group to ZIP files. You simply configure the group id and access token and this image will download all repositories to separate zip files.

For simplicity, it will save all files into a single directory, using the full path of the group structure to name the files. The container assumes the volume mapping to a `/data` directory within the container that should be mapped at runtime.

> __Note__: This process only archives the file content of the repository and does not backup full commit history, issues, or other content within the repository.

# How to use this image

## Using with an environment variable file

The image can be run by passing an environment variable file to `docker run`.

```console
$ docker run -ti --rm --name gitlab-backup --env-file ./env.list -v /your/local/directory:/data cscheide/gitlab-group-projects-backup:latest
```

There is a [sample.env](https://github.com/crscheid/gitlab-group-projects-backup/blob/main/sample.env) file contained within the Github project for you to reference if needed.

## Using with environment variables

Alternatively, the environment variables can be passed in via the `-e` flag.

```console
$ docker run -ti --rm --name gitlab-backup -e "GITLAB_TOKEN=your_gitlab_token" -e "GITLAB_GROUP_ID=000000" -e "BACKUP_ARCHIVED=yes" -v /your/local/directory:/data cscheide/gitlab-group-projects-backup:latest
```

# Configuration

This container utilizes environment variables for configuration. The following shows the required and optional environment variables

## Required Variables

The following environment variables are minimally required in order for the container to work properly:

- `GITLAB_TOKEN` : The Gitlab access token of a user who has access to the group
- `GITLAB_GROUP_ID` : The ID of the Gitlab group to back backed up

## Optional Variables

In addition, the container supports the optional configurations:

- `BACKUP_ARCHIVED` : If this variable is set to `yes`, repositories that are archived will also be backed up.

## Data Directory

The container will write the backup ZIP files to the `/data` directory within the container. In most cases, you will want to map this directory to a local file directory to keep the backups.


# Feedback / Contribution

## Issues

If you have any problems with or questions about this image, please post a [GitHub issue](https://github.com/crscheid/gitlab-group-projects-backup/issues).

## Contributing

This started out as a project for a particular issue that I had. However, anyone is invited to contribute new features, fixes, or updates, large or small; I will be happy to receive any ideas on how to make this better. Please feel free to fork or submit pull requests.

Before you start to tackle a new issue, please discuss your plans through a [GitHub issue](https://github.com/crscheid/gitlab-group-projects-backup/issues), especially for more ambitious contributions. This gives other contributors a chance to point you in the right direction, give you feedback on your design, and help you find out if someone else is working on the same thing.
