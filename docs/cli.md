---
title: Using the CLI
---
# Using the Task Badger CLI

The CLI (command line interface) is a tool that allows you to interface with
Task Badger via the shell. This makes it easy to integrate it into workflows
without the need to write any code.

## Configuration

The CLI requires the same configuration as the API. This can be provided in one of
three ways (in order of precedence):

1. Command line arguments
2. Environment variables
3. Config file

Values provided via environment variables override values in the configuration file
and values provided via the command line override both environment config and the
configuration file.

Details about the configuration parameters can be found [here](basics.md#organization-and-project)

### Command line arguments

Running `taskbadger -h` will show you the command line help. 
  
```bash
 $ taskbadger -h
                                                                                                            
 Usage: taskbadger [OPTIONS] COMMAND [ARGS]...                                                              
                                                                                                            
 Task Badger CLI                                                                                            
                                                                                                            
╭─ Options ──────────────────────────────────────╮
│ --org                 -o   TASKBADGER_ORG      │
│                                                │
│ --project             -p   TASKBADGER_PROJECT  │
╰────────────────────────────────────────────────╯
```

The API Key can not be provided via the command line as a security measure to prevent logging
of the API Key.

### Environment variables

Use the following environment variable names to configure the CLI:

```
TASKBADGER_API_KEY
TASKBADGER_ORG
TASKBADGER_PROJECT
```

### Configuration file

The CLI includes a convenience command to create the configuration file. Running the `configure`
command will prompt you for the configuration parameters and save them to the configuration
file.

```bash
$ taskbadger configure

Organization slug: my-org 
Project slug: project-x 
API Key: XYZ.ABC 

Config written to ~/.config/taskbadger/config
```