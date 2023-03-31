# Copyright (C) Lutra Consulting Limited
#
# SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial

""" Base migration for CE, reflects the state of release 2021.6.1

Revision ID: 2686074eff45
Revises: 
Create Date: 2022-12-15 10:40:42.234210

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "2686074eff45"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "account",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "type",
            postgresql.ENUM("user", "organisation", name="account_type"),
            nullable=False,
        ),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_account")),
    )
    op.create_index(op.f("ix_account_owner_id"), "account", ["owner_id"], unique=False)
    op.create_index(op.f("ix_account_type"), "account", ["type"], unique=False)
    op.create_table(
        "login_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("user_agent", sa.String(), nullable=True),
        sa.Column("ip_address", sa.String(), nullable=True),
        sa.Column("ip_geolocation_country", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_login_history")),
    )
    op.create_index(
        op.f("ix_login_history_ip_address"),
        "login_history",
        ["ip_address"],
        unique=False,
    )
    op.create_index(
        op.f("ix_login_history_ip_geolocation_country"),
        "login_history",
        ["ip_geolocation_country"],
        unique=False,
    )
    op.create_index(
        op.f("ix_login_history_timestamp"), "login_history", ["timestamp"], unique=False
    )
    op.create_index(
        op.f("ix_login_history_user_agent"),
        "login_history",
        ["user_agent"],
        unique=False,
    )
    op.create_index(
        op.f("ix_login_history_username"), "login_history", ["username"], unique=False
    )
    op.create_table(
        "organisation",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "owners", postgresql.ARRAY(sa.Integer()), server_default="{}", nullable=True
        ),
        sa.Column(
            "admins", postgresql.ARRAY(sa.Integer()), server_default="{}", nullable=True
        ),
        sa.Column(
            "writers",
            postgresql.ARRAY(sa.Integer()),
            server_default="{}",
            nullable=True,
        ),
        sa.Column(
            "readers",
            postgresql.ARRAY(sa.Integer()),
            server_default="{}",
            nullable=True,
        ),
        sa.Column("registration_date", sa.DateTime(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.Column("inactive_since", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_organisation")),
        sa.UniqueConstraint("name", name=op.f("uq_organisation_name")),
    )
    op.create_index(
        "ix_org_admins",
        "organisation",
        ["admins"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_index(
        "ix_org_owners",
        "organisation",
        ["owners"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_index(
        "ix_org_readers",
        "organisation",
        ["readers"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_index(
        "ix_org_writers",
        "organisation",
        ["writers"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_index(
        op.f("ix_organisation_inactive_since"),
        "organisation",
        ["inactive_since"],
        unique=False,
    )
    op.create_index(
        op.f("ix_organisation_name"), "organisation", ["name"], unique=False
    )
    op.create_table(
        "removed_project",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("namespace", sa.String(), nullable=False),
        sa.Column("properties", sa.JSON(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("removed_by", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_removed_project")),
    )
    op.create_index(
        op.f("ix_removed_project_name"), "removed_project", ["name"], unique=False
    )
    op.create_index(
        op.f("ix_removed_project_namespace"),
        "removed_project",
        ["namespace"],
        unique=False,
    )
    op.create_index(
        op.f("ix_removed_project_timestamp"),
        "removed_project",
        ["timestamp"],
        unique=False,
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=True),
        sa.Column("email", sa.String(length=120), nullable=True),
        sa.Column("passwd", sa.String(length=80), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.Column("is_admin", sa.Boolean(), nullable=True),
        sa.Column("verified_email", sa.Boolean(), nullable=True),
        sa.Column("inactive_since", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user")),
        sa.UniqueConstraint("email", name=op.f("uq_user_email")),
        sa.UniqueConstraint("username", name=op.f("uq_user_username")),
    )
    op.create_index(
        op.f("ix_user_inactive_since"), "user", ["inactive_since"], unique=False
    )
    op.create_table(
        "namespace",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=True),
        sa.Column("storage", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.id"],
            name=op.f("fk_namespace_account_id_account"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("name", name=op.f("pk_namespace")),
    )
    op.create_table(
        "organisation_invitation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("org_name", sa.String(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column(
            "role",
            postgresql.ENUM("reader", "writer", "admin", "owner", name="role"),
            nullable=False,
        ),
        sa.Column("expire", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["org_name"],
            ["organisation.name"],
            name=op.f("fk_organisation_invitation_org_name_organisation"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["username"],
            ["user.username"],
            name=op.f("fk_organisation_invitation_username_user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_organisation_invitation")),
    )
    op.create_table(
        "user_profile",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("receive_notifications", sa.Boolean(), nullable=True),
        sa.Column("first_name", sa.String(length=256), nullable=True),
        sa.Column("last_name", sa.String(length=256), nullable=True),
        sa.Column("registration_date", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("fk_user_profile_user_id_user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_user_profile")),
    )
    op.create_index(
        op.f("ix_user_profile_receive_notifications"),
        "user_profile",
        ["receive_notifications"],
        unique=False,
    )
    op.create_table(
        "project",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("storage_params", sa.JSON(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=True),
        sa.Column("creator_id", sa.Integer(), nullable=True),
        sa.Column("updated", sa.DateTime(), nullable=True),
        sa.Column("files", sa.JSON(), nullable=True),
        sa.Column(
            "tags", postgresql.ARRAY(sa.String()), server_default="{}", nullable=True
        ),
        sa.Column("disk_usage", sa.BIGINT(), nullable=False),
        sa.Column("latest_version", sa.String(), nullable=True),
        sa.Column("namespace", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["creator_id"], ["user.id"], name=op.f("fk_project_creator_id_user")
        ),
        sa.ForeignKeyConstraint(
            ["namespace"],
            ["namespace.name"],
            name=op.f("fk_project_namespace_namespace"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_project")),
        sa.UniqueConstraint("name", "namespace", name=op.f("uq_project_name")),
    )
    op.create_index(op.f("ix_project_created"), "project", ["created"], unique=False)
    op.create_index(
        op.f("ix_project_creator_id"), "project", ["creator_id"], unique=False
    )
    op.create_index(
        op.f("ix_project_latest_version"), "project", ["latest_version"], unique=False
    )
    op.create_index(op.f("ix_project_name"), "project", ["name"], unique=False)
    op.create_index(
        op.f("ix_project_namespace"), "project", ["namespace"], unique=False
    )
    op.create_table(
        "access_request",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("namespace", sa.String(), nullable=False),
        sa.Column("expire", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
            name=op.f("fk_access_request_project_id_project"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("fk_access_request_user_id_user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_access_request")),
    )
    op.create_index(
        op.f("ix_access_request_namespace"),
        "access_request",
        ["namespace"],
        unique=False,
    )
    op.create_index(
        op.f("ix_access_request_project_id"),
        "access_request",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_access_request_user_id"), "access_request", ["user_id"], unique=False
    )
    op.create_table(
        "project_access",
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("public", sa.Boolean(), nullable=True),
        sa.Column(
            "owners", postgresql.ARRAY(sa.Integer()), server_default="{}", nullable=True
        ),
        sa.Column(
            "readers",
            postgresql.ARRAY(sa.Integer()),
            server_default="{}",
            nullable=True,
        ),
        sa.Column(
            "writers",
            postgresql.ARRAY(sa.Integer()),
            server_default="{}",
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
            name=op.f("fk_project_access_project_id_project"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("project_id", name=op.f("pk_project_access")),
    )
    op.create_index(
        "ix_project_access_owners",
        "project_access",
        ["owners"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_index(
        op.f("ix_project_access_project_id"),
        "project_access",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_access_public"), "project_access", ["public"], unique=False
    )
    op.create_index(
        "ix_project_access_readers",
        "project_access",
        ["readers"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_index(
        "ix_project_access_writers",
        "project_access",
        ["writers"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_table(
        "project_transfer",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("from_ns_name", sa.String(), nullable=False),
        sa.Column("to_ns_name", sa.String(), nullable=False),
        sa.Column("requested_by", sa.Integer(), nullable=True),
        sa.Column("expire", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
            name=op.f("fk_project_transfer_project_id_project"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["requested_by"],
            ["user.id"],
            name=op.f("fk_project_transfer_requested_by_user"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["to_ns_name"],
            ["namespace.name"],
            name=op.f("fk_project_transfer_to_ns_name_namespace"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_project_transfer")),
        sa.UniqueConstraint("project_id", name=op.f("uq_project_transfer_project_id")),
    )
    op.create_index(
        op.f("ix_project_transfer_from_ns_name"),
        "project_transfer",
        ["from_ns_name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_transfer_project_id"),
        "project_transfer",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_transfer_to_ns_name"),
        "project_transfer",
        ["to_ns_name"],
        unique=False,
    )
    op.create_table(
        "project_version",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=True),
        sa.Column("author", sa.String(), nullable=True),
        sa.Column("changes", sa.JSON(), nullable=True),
        sa.Column("files", sa.JSON(), nullable=True),
        sa.Column("user_agent", sa.String(), nullable=True),
        sa.Column("ip_address", sa.String(), nullable=True),
        sa.Column("ip_geolocation_country", sa.String(), nullable=True),
        sa.Column("project_size", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
            name=op.f("fk_project_version_project_id_project"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_project_version")),
    )
    op.create_index(
        op.f("ix_project_version_author"), "project_version", ["author"], unique=False
    )
    op.create_index(
        op.f("ix_project_version_created"), "project_version", ["created"], unique=False
    )
    op.create_index(
        op.f("ix_project_version_ip_address"),
        "project_version",
        ["ip_address"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_version_ip_geolocation_country"),
        "project_version",
        ["ip_geolocation_country"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_version_name"), "project_version", ["name"], unique=False
    )
    op.create_index(
        op.f("ix_project_version_project_id"),
        "project_version",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_version_project_size"),
        "project_version",
        ["project_size"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_version_user_agent"),
        "project_version",
        ["user_agent"],
        unique=False,
    )
    op.create_table(
        "upload",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.Column("changes", sa.JSON(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
            name=op.f("fk_upload_project_id_project"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("fk_upload_user_id_user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_upload")),
        sa.UniqueConstraint("project_id", "version", name=op.f("uq_upload_project_id")),
    )
    op.create_index(
        op.f("ix_upload_project_id"), "upload", ["project_id"], unique=False
    )
    op.create_index(op.f("ix_upload_version"), "upload", ["version"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_upload_version"), table_name="upload")
    op.drop_index(op.f("ix_upload_project_id"), table_name="upload")
    op.drop_table("upload")
    op.drop_index(op.f("ix_project_version_user_agent"), table_name="project_version")
    op.drop_index(op.f("ix_project_version_project_size"), table_name="project_version")
    op.drop_index(op.f("ix_project_version_project_id"), table_name="project_version")
    op.drop_index(op.f("ix_project_version_name"), table_name="project_version")
    op.drop_index(
        op.f("ix_project_version_ip_geolocation_country"), table_name="project_version"
    )
    op.drop_index(op.f("ix_project_version_ip_address"), table_name="project_version")
    op.drop_index(op.f("ix_project_version_created"), table_name="project_version")
    op.drop_index(op.f("ix_project_version_author"), table_name="project_version")
    op.drop_table("project_version")
    op.drop_index(op.f("ix_project_transfer_to_ns_name"), table_name="project_transfer")
    op.drop_index(op.f("ix_project_transfer_project_id"), table_name="project_transfer")
    op.drop_index(
        op.f("ix_project_transfer_from_ns_name"), table_name="project_transfer"
    )
    op.drop_table("project_transfer")
    op.drop_index("ix_project_access_writers", table_name="project_access")
    op.drop_index("ix_project_access_readers", table_name="project_access")
    op.drop_index(op.f("ix_project_access_public"), table_name="project_access")
    op.drop_index(op.f("ix_project_access_project_id"), table_name="project_access")
    op.drop_index("ix_project_access_owners", table_name="project_access")
    op.drop_table("project_access")
    op.drop_index(op.f("ix_access_request_user_id"), table_name="access_request")
    op.drop_index(op.f("ix_access_request_project_id"), table_name="access_request")
    op.drop_index(op.f("ix_access_request_namespace"), table_name="access_request")
    op.drop_table("access_request")
    op.drop_index(op.f("ix_project_namespace"), table_name="project")
    op.drop_index(op.f("ix_project_name"), table_name="project")
    op.drop_index(op.f("ix_project_latest_version"), table_name="project")
    op.drop_index(op.f("ix_project_creator_id"), table_name="project")
    op.drop_index(op.f("ix_project_created"), table_name="project")
    op.drop_table("project")
    op.drop_index(
        op.f("ix_user_profile_receive_notifications"), table_name="user_profile"
    )
    op.drop_table("user_profile")
    op.drop_table("organisation_invitation")
    op.drop_table("namespace")
    op.drop_index(op.f("ix_user_inactive_since"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_removed_project_timestamp"), table_name="removed_project")
    op.drop_index(op.f("ix_removed_project_namespace"), table_name="removed_project")
    op.drop_index(op.f("ix_removed_project_name"), table_name="removed_project")
    op.drop_table("removed_project")
    op.drop_index(op.f("ix_organisation_name"), table_name="organisation")
    op.drop_index(op.f("ix_organisation_inactive_since"), table_name="organisation")
    op.drop_index("ix_org_writers", table_name="organisation")
    op.drop_index("ix_org_readers", table_name="organisation")
    op.drop_index("ix_org_owners", table_name="organisation")
    op.drop_index("ix_org_admins", table_name="organisation")
    op.drop_table("organisation")
    op.drop_index(op.f("ix_login_history_username"), table_name="login_history")
    op.drop_index(op.f("ix_login_history_user_agent"), table_name="login_history")
    op.drop_index(op.f("ix_login_history_timestamp"), table_name="login_history")
    op.drop_index(
        op.f("ix_login_history_ip_geolocation_country"), table_name="login_history"
    )
    op.drop_index(op.f("ix_login_history_ip_address"), table_name="login_history")
    op.drop_table("login_history")
    op.drop_index(op.f("ix_account_type"), table_name="account")
    op.drop_index(op.f("ix_account_owner_id"), table_name="account")
    op.drop_table("account")
    # ### end Alembic commands ###