"""
Loads configuration settings from environment variables and command line arguments

It should be loaded first, and then passed to the other managers and classes that need it.

Responsibilities:
- Load environment variables
- Load command line arguments

Implemented for AWS and Neo4j, but can be extended to other services

TODO: Implement a configuration file to allow for more complex configurations
TODO: Query the user for missing configuration settings
"""

import argparse
from dataclasses import dataclass
import os
from dotenv import load_dotenv

from network_visualizer.lib.config import boto_config, neo4j_config


@dataclass
class Settings:
    aws_profile: str
    aws_region: str


class ConfigurationManager:
    settings: Settings = {}

    def __init__(self):
        # Attempt to load environment variables from a .env file if present
        load_dotenv()
        self.apply_default_settings()
        self.load_environment_variables()
        self.load_command_line_arguments()

    def apply_default_settings(self):
        """Apply default settings from configuration files."""
        # Assume boto_config and neo4j_config are already defined or imported
        self.settings.update(
            {
                "neo4j_uri": neo4j_config["uri"],
                "neo4j_user": neo4j_config["user"],
                "neo4j_password": neo4j_config["password"],
                # For Boto3, we keep the configuration object directly
                "boto_config": boto_config,
            }
        )

    def load_environment_variables(self):
        """Override settings with environment variables."""
        # List of AWS and Neo4j environment variable names
        env_vars = [
            "aws_profile",
            "aws_region",
            "aws_output",
            "aws_access_key_id",
            "aws_secret_access_key",
            "aws_session_token",
            "neo4j_uri",
            "neo4j_user",
            "neo4j_password",
        ]

        # Update settings with environment variables if they are set
        for var in env_vars:
            value = os.getenv(var.upper())
            if value is not None:
                self.settings[var] = value

    def load_command_line_arguments(self):
        def load_aws_command_line_arguments(self):
            parser = argparse.ArgumentParser(description="AWS Service Manager")
            parser.add_argument("--aws-profile", help="AWS Profile to use")
            parser.add_argument("--aws-region", help="AWS Region to use")
            parser.add_argument("--aws-output", help="AWS Output to use")
            parser.add_argument("--aws-access-key-id", help="AWS Access Key ID to use")
            parser.add_argument(
                "--aws-secret-access-key", help="AWS Secret Access Key to use"
            )
            parser.add_argument("--aws-session-token", help="AWS Session Token to use")
            args = parser.parse_args()

            if args.aws_profile:
                self.settings["aws_profile"] = args.aws_profile
            if args.aws_region:
                self.settings["aws_region"] = args.aws_region
            if args.aws_output:
                self.settings["aws_output"] = args.aws_output
            if args.aws_access_key_id:
                self.settings["aws_access_key_id"] = args.aws_access_key_id
            if args.aws_secret_access_key:
                self.settings["aws_secret_access_key"] = args.aws_secret_access_key
            if args.aws_session_token:
                self.settings["aws_session_token"] = args.aws_session_token

        def load_neo4j_command_line_arguments(self):
            parser = argparse.ArgumentParser(description="Neo4j Database Manager")
            parser.add_argument("--neo4j-uri", help="Neo4j URI to use")
            parser.add_argument("--neo4j-user", help="Neo4j User to use")
            parser.add_argument("--neo4j-password", help="Neo4j Password to use")
            args = parser.parse_args()

            if args.neo4j_uri:
                self.settings["neo4j_uri"] = args.neo4j_uri
            if args.neo4j_user:
                self.settings["neo4j_user"] = args.neo4j_user
            if args.neo4j_password:
                self.settings["neo4j_password"] = args.neo4j_password

        load_aws_command_line_arguments(self)
        load_neo4j_command_line_arguments(self)

    def get_configuration(self):
        return self.settings
