# GENERATED FILE — do not edit by hand.
# Source: the VAIF Studio API's OpenAPI description, sha256:615e77b7a0789543; 775 operations generated, 168 not generated (listed in UNGENERATED_OPERATIONS with the reason).
# Changes are made in the generator, not in this file; see CONTRIBUTING.md.
"""One coroutine per operation, generated from the VAIF Studio API's OpenAPI description."""

from __future__ import annotations

from typing import Any, Mapping, Optional, cast

from vaifstudio._generated.operations import OPERATIONS
from vaifstudio._operations import OperationsBase


class Operations(OperationsBase):
    """The typed operation surface under the hand-written modules.

    Every method sends the request as the signed-in user (if any) through
    the client's transport, so it carries the project key, retries and
    error mapping. JSON responses are decoded; ``binary`` operations return
    ``bytes`` (a redirect to a signed link is read without the project key
    or the session token), and ``sse`` operations return the
    ``httpx.Response`` after the stream has ended, with the whole body read.
    """

    async def delete_ai_copilot_session_by_session_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /ai/copilot/session/{sessionId}"""
        return await self._call(
            OPERATIONS["delete_ai_copilot_session_by_session_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_alert_rules_by_rule_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /alert-rules/{ruleId}"""
        return await self._call(
            OPERATIONS["delete_alert_rules_by_rule_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_auth_me_linked_accounts_by_provider(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /auth/me/linked-accounts/{provider}"""
        return await self._call(
            OPERATIONS["delete_auth_me_linked_accounts_by_provider"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_auth_sessions_by_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /auth/sessions/{id}"""
        return await self._call(
            OPERATIONS["delete_auth_sessions_by_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_billing_org_by_org_id_addons_by_addon_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /billing/org/{orgId}/addons/{addonId}"""
        return await self._call(
            OPERATIONS["delete_billing_org_by_org_id_addons_by_addon_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_billing_org_by_org_id_contacts_by_contact_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /billing/org/{orgId}/contacts/{contactId}"""
        return await self._call(
            OPERATIONS["delete_billing_org_by_org_id_contacts_by_contact_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_billing_org_by_org_id_usage_alerts_by_alert_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /billing/org/{orgId}/usage-alerts/{alertId}"""
        return await self._call(
            OPERATIONS["delete_billing_org_by_org_id_usage_alerts_by_alert_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_buckets_by_bucket_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /buckets/{bucketId}"""
        return await self._call(
            OPERATIONS["delete_buckets_by_bucket_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_buckets_by_bucket_id_files(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /buckets/{bucketId}/files"""
        return await self._call(
            OPERATIONS["delete_buckets_by_bucket_id_files"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def delete_database_extensions_project_by_project_id_by_extension_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /database/extensions/project/{projectId}/{extensionId}"""
        return await self._call(
            OPERATIONS["delete_database_extensions_project_by_project_id_by_extension_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def delete_database_wrappers_project_by_project_id_by_wrapper_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /database/wrappers/project/{projectId}/{wrapperId}"""
        return await self._call(
            OPERATIONS["delete_database_wrappers_project_by_project_id_by_wrapper_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def delete_functions_by_function_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /functions/{functionId}"""
        return await self._call(
            OPERATIONS["delete_functions_by_function_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_functions_by_function_id_schedule(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /functions/{functionId}/schedule"""
        return await self._call(
            OPERATIONS["delete_functions_by_function_id_schedule"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_functions_secrets_by_secret_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /functions/secrets/{secretId}"""
        return await self._call(
            OPERATIONS["delete_functions_secrets_by_secret_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_functions_triggers_by_trigger_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /functions/triggers/{triggerId}"""
        return await self._call(
            OPERATIONS["delete_functions_triggers_by_trigger_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_generated_by_table_bulk(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /generated/{table}/bulk"""
        return await self._call(
            OPERATIONS["delete_generated_by_table_bulk"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def delete_generated_by_table_by_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /generated/{table}/{id}"""
        return await self._call(
            OPERATIONS["delete_generated_by_table_by_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_integrations_subscriptions_by_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /integrations/subscriptions/{id}"""
        return await self._call(
            OPERATIONS["delete_integrations_subscriptions_by_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_mcp_connections_by_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /mcp/connections/{id}"""
        return await self._call(
            OPERATIONS["delete_mcp_connections_by_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_mongodb_by_collection_indexes_by_index_name(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /mongodb/{collection}/indexes/{indexName}"""
        return await self._call(
            OPERATIONS["delete_mongodb_by_collection_indexes_by_index_name"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_mongodb_collections_by_name(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /mongodb/collections/{name}"""
        return await self._call(
            OPERATIONS["delete_mongodb_collections_by_name"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_oauth_org_by_org_id_provider_by_provider(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /oauth/org/{orgId}/provider/{provider}"""
        return await self._call(
            OPERATIONS["delete_oauth_org_by_org_id_provider_by_provider"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_orgs_by_org_id_invites_by_invite_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /orgs/{orgId}/invites/{inviteId}"""
        return await self._call(
            OPERATIONS["delete_orgs_by_org_id_invites_by_invite_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_orgs_by_org_id_leave_requests_mine(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /orgs/{orgId}/leave-requests/mine"""
        return await self._call(
            OPERATIONS["delete_orgs_by_org_id_leave_requests_mine"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_orgs_by_org_id_members_by_user_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /orgs/{orgId}/members/{userId}"""
        return await self._call(
            OPERATIONS["delete_orgs_by_org_id_members_by_user_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_orgs_by_org_id_transfers_by_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /orgs/{orgId}/transfers/{id}"""
        return await self._call(
            OPERATIONS["delete_orgs_by_org_id_transfers_by_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_projects_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /projects/{projectId}"""
        return await self._call(
            OPERATIONS["delete_projects_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_projects_by_project_id_auth_oauth_apps_by_provider(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /projects/{projectId}/auth/oauth-apps/{provider}"""
        return await self._call(
            OPERATIONS["delete_projects_by_project_id_auth_oauth_apps_by_provider"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_projects_by_project_id_auth_sessions(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /projects/{projectId}/auth/sessions"""
        return await self._call(
            OPERATIONS["delete_projects_by_project_id_auth_sessions"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_projects_by_project_id_auth_sessions_by_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /projects/{projectId}/auth/sessions/{id}"""
        return await self._call(
            OPERATIONS["delete_projects_by_project_id_auth_sessions_by_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_projects_by_project_id_branches_by_branch_name(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /projects/{projectId}/branches/{branchName}"""
        return await self._call(
            OPERATIONS["delete_projects_by_project_id_branches_by_branch_name"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_projects_by_project_id_database_dedicated(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /projects/{projectId}/database/dedicated"""
        return await self._call(
            OPERATIONS["delete_projects_by_project_id_database_dedicated"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_projects_by_project_id_env_vars_by_env_var_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /projects/{projectId}/env-vars/{envVarId}"""
        return await self._call(
            OPERATIONS["delete_projects_by_project_id_env_vars_by_env_var_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_projects_by_project_id_environments_by_env_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /projects/{projectId}/environments/{envId}"""
        return await self._call(
            OPERATIONS["delete_projects_by_project_id_environments_by_env_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_projects_by_project_id_environments_by_env_id_domains_by_domain_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /projects/{projectId}/environments/{envId}/domains/{domainId}"""
        return await self._call(
            OPERATIONS["delete_projects_by_project_id_environments_by_env_id_domains_by_domain_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_projects_by_project_id_github_disconnect(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /projects/{projectId}/github/disconnect"""
        return await self._call(
            OPERATIONS["delete_projects_by_project_id_github_disconnect"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_projects_by_project_id_infrastructure_by_instance_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /projects/{projectId}/infrastructure/{instanceId}"""
        return await self._call(
            OPERATIONS["delete_projects_by_project_id_infrastructure_by_instance_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def delete_projects_by_project_id_members_by_user_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /projects/{projectId}/members/{userId}"""
        return await self._call(
            OPERATIONS["delete_projects_by_project_id_members_by_user_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_projects_by_project_id_users_by_user_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /projects/{projectId}/users/{userId}"""
        return await self._call(
            OPERATIONS["delete_projects_by_project_id_users_by_user_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_projects_by_project_id_users_by_user_id_sessions_by_session_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /projects/{projectId}/users/{userId}/sessions/{sessionId}"""
        return await self._call(
            OPERATIONS["delete_projects_by_project_id_users_by_user_id_sessions_by_session_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_rls_policies_by_policy_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /rls/policies/{policyId}"""
        return await self._call(
            OPERATIONS["delete_rls_policies_by_policy_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_schema_engine_snippets_by_project_id_by_snippet_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /schema-engine/snippets/{projectId}/{snippetId}"""
        return await self._call(
            OPERATIONS["delete_schema_engine_snippets_by_project_id_by_snippet_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_services_by_service_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /services/{serviceId}"""
        return await self._call(
            OPERATIONS["delete_services_by_service_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_services_by_service_id_domains_by_domain_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /services/{serviceId}/domains/{domainId}"""
        return await self._call(
            OPERATIONS["delete_services_by_service_id_domains_by_domain_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_services_by_service_id_git_connect(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /services/{serviceId}/git/connect"""
        return await self._call(
            OPERATIONS["delete_services_by_service_id_git_connect"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_sso_org_by_org_id_connections_by_connection_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /sso/org/{orgId}/connections/{connectionId}"""
        return await self._call(
            OPERATIONS["delete_sso_org_by_org_id_connections_by_connection_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_sso_org_by_org_id_connections_by_connection_id_certificates_by_cert_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /sso/org/{orgId}/connections/{connectionId}/certificates/{certId}"""
        return await self._call(
            OPERATIONS["delete_sso_org_by_org_id_connections_by_connection_id_certificates_by_cert_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_sso_org_by_org_id_connections_by_connection_id_identities_by_user_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /sso/org/{orgId}/connections/{connectionId}/identities/{userId}"""
        return await self._call(
            OPERATIONS["delete_sso_org_by_org_id_connections_by_connection_id_identities_by_user_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_sso_org_by_org_id_connections_by_connection_id_scim_tokens_by_token_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /sso/org/{orgId}/connections/{connectionId}/scim/tokens/{tokenId}"""
        return await self._call(
            OPERATIONS["delete_sso_org_by_org_id_connections_by_connection_id_scim_tokens_by_token_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_sso_org_by_org_id_outside_members_allow_by_allow_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /sso/org/{orgId}/outside-members/allow/{allowId}"""
        return await self._call(
            OPERATIONS["delete_sso_org_by_org_id_outside_members_allow_by_allow_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_sso_org_by_org_id_security_contact(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /sso/org/{orgId}/security-contact"""
        return await self._call(
            OPERATIONS["delete_sso_org_by_org_id_security_contact"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_storage_buckets_by_bucket_id_policies_by_policy_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /storage/buckets/{bucketId}/policies/{policyId}"""
        return await self._call(
            OPERATIONS["delete_storage_buckets_by_bucket_id_policies_by_policy_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_templates_by_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /templates/{id}"""
        return await self._call(
            OPERATIONS["delete_templates_by_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def delete_v1_data_by_project_id_by_table_bulk(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /v1/data/{projectId}/{table}/bulk"""
        return await self._call(
            OPERATIONS["delete_v1_data_by_project_id_by_table_bulk"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def delete_v1_data_by_project_id_by_table_by_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """DELETE /v1/data/{projectId}/{table}/{id}"""
        return await self._call(
            OPERATIONS["delete_v1_data_by_project_id_by_table_by_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /"""
        return await self._call(
            OPERATIONS["get"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_activation_org_by_org_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /activation/org/{orgId}"""
        return await self._call(
            OPERATIONS["get_activation_org_by_org_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_autocomplete(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/autocomplete"""
        return await self._call(
            OPERATIONS["get_ai_copilot_autocomplete"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_context_summary_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/context-summary/{projectId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_context_summary_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_credit_status_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/credit-status/{projectId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_credit_status_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_deploy_by_deploy_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/deploy/{deployId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_deploy_by_deploy_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_deploy_history_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/deploy/history/{projectId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_deploy_history_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_execution_by_execution_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/execution/{executionId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_execution_by_execution_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_executions_by_session_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/executions/{sessionId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_executions_by_session_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_git_branches_by_session_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/git/branches/{sessionId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_git_branches_by_session_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_git_files_by_session_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/git/files/{sessionId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_git_files_by_session_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_git_log_by_session_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/git/log/{sessionId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_git_log_by_session_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_git_status_by_session_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/git/status/{sessionId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_git_status_by_session_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_job_by_job_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/job/{jobId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_job_by_job_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_manifest_by_manifest_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/manifest/{manifestId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_manifest_by_manifest_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_metrics_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/metrics/{projectId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_metrics_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_metrics_org_by_org_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/metrics/org/{orgId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_metrics_org_by_org_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_models_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/models/{projectId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_models_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_session_by_session_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/session/{sessionId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_session_by_session_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_session_by_session_id_editor_files(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/session/{sessionId}/editor-files"""
        return await self._call(
            OPERATIONS["get_ai_copilot_session_by_session_id_editor_files"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_session_by_session_id_workspace_export(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/session/{sessionId}/workspace/export"""
        return await self._call(
            OPERATIONS["get_ai_copilot_session_by_session_id_workspace_export"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_session_by_session_id_workspace_status(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/session/{sessionId}/workspace/status"""
        return await self._call(
            OPERATIONS["get_ai_copilot_session_by_session_id_workspace_status"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_session_by_session_id_workspace_types(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/session/{sessionId}/workspace/types"""
        return await self._call(
            OPERATIONS["get_ai_copilot_session_by_session_id_workspace_types"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_sessions_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/sessions/{projectId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_sessions_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_usage_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/usage/{projectId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_usage_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_usage_org_by_org_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/usage-org/{orgId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_usage_org_by_org_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_version_by_version_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/version/{versionId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_version_by_version_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_version_by_version_id_diff_by_compare_version_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/version/{versionId}/diff/{compareVersionId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_version_by_version_id_diff_by_compare_version_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_copilot_versions_by_session_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai/copilot/versions/{sessionId}"""
        return await self._call(
            OPERATIONS["get_ai_copilot_versions_by_session_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_usage_org_by_org_id_breakdown(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai-usage/org/{orgId}/breakdown"""
        return await self._call(
            OPERATIONS["get_ai_usage_org_by_org_id_breakdown"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_usage_org_by_org_id_exhaustion_events(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai-usage/org/{orgId}/exhaustion-events"""
        return await self._call(
            OPERATIONS["get_ai_usage_org_by_org_id_exhaustion_events"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_ai_usage_org_by_org_id_history(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai-usage/org/{orgId}/history"""
        return await self._call(
            OPERATIONS["get_ai_usage_org_by_org_id_history"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_ai_usage_org_by_org_id_recent(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai-usage/org/{orgId}/recent"""
        return await self._call(
            OPERATIONS["get_ai_usage_org_by_org_id_recent"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_ai_usage_org_by_org_id_rollups(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai-usage/org/{orgId}/rollups"""
        return await self._call(
            OPERATIONS["get_ai_usage_org_by_org_id_rollups"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_ai_usage_org_by_org_id_summary(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai-usage/org/{orgId}/summary"""
        return await self._call(
            OPERATIONS["get_ai_usage_org_by_org_id_summary"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_ai_usage_org_by_org_id_verament(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /ai-usage/org/{orgId}/verament"""
        return await self._call(
            OPERATIONS["get_ai_usage_org_by_org_id_verament"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_alert_rules_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /alert-rules/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_alert_rules_project_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_announcements(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /announcements"""
        return await self._call(
            OPERATIONS["get_announcements"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_audit_org_by_org_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /audit/org/{orgId}"""
        return await self._call(
            OPERATIONS["get_audit_org_by_org_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_audit_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /audit/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_audit_project_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_auth_me(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /auth/me"""
        return await self._call(
            OPERATIONS["get_auth_me"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_auth_me_admin(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /auth/me/admin"""
        return await self._call(
            OPERATIONS["get_auth_me_admin"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_auth_me_context(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /auth/me/context"""
        return await self._call(
            OPERATIONS["get_auth_me_context"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_auth_me_linked_accounts(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /auth/me/linked-accounts"""
        return await self._call(
            OPERATIONS["get_auth_me_linked_accounts"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_auth_mfa_status(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /auth/mfa/status"""
        return await self._call(
            OPERATIONS["get_auth_mfa_status"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_auth_oauth_providers(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /auth/oauth/providers"""
        return await self._call(
            OPERATIONS["get_auth_oauth_providers"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_auth_session(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /auth/session"""
        return await self._call(
            OPERATIONS["get_auth_session"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_auth_sessions(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /auth/sessions"""
        return await self._call(
            OPERATIONS["get_auth_sessions"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_auth_tenant_session(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /auth/tenant/session"""
        return await self._call(
            OPERATIONS["get_auth_tenant_session"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_addons_catalog(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/addons/catalog"""
        return await self._call(
            OPERATIONS["get_billing_addons_catalog"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_billing_checkout_verify_by_session_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/checkout/verify/{sessionId}"""
        return await self._call(
            OPERATIONS["get_billing_checkout_verify_by_session_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_credits_packages(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/credits/packages"""
        return await self._call(
            OPERATIONS["get_billing_credits_packages"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_credits_rates(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/credits/rates"""
        return await self._call(
            OPERATIONS["get_billing_credits_rates"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_founders_wall(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/founders/wall"""
        return await self._call(
            OPERATIONS["get_billing_founders_wall"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_addons(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/addons"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_addons"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_card_check(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/card-check"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_card_check"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_contacts(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/contacts"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_contacts"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_cost_breakdown(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/cost-breakdown"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_cost_breakdown"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_credits_auto_topup(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/credits/auto-topup"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_credits_auto_topup"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_credits_transactions(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/credits/transactions"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_credits_transactions"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_founder(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/founder"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_founder"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_hosting(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/hosting"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_hosting"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_infrastructure(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/infrastructure"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_infrastructure"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_invoices(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/invoices"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_invoices"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_overages(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/overages"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_overages"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_overages_history(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/overages/history"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_overages_history"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_subscription(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/subscription"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_subscription"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_summary(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/summary"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_summary"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_tax_info(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/tax-info"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_tax_info"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_usage(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/usage"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_usage"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_usage_alerts(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/usage-alerts"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_usage_alerts"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_usage_alerts_configured(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/usage-alerts/configured"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_usage_alerts_configured"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_usage_alerts_history(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/usage-alerts/history"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_usage_alerts_history"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_usage_history(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/usage/history"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_usage_history"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_billing_org_by_org_id_usage_realtime(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/org/{orgId}/usage/realtime"""
        return await self._call(
            OPERATIONS["get_billing_org_by_org_id_usage_realtime"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_billing_plans(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /billing/plans"""
        return await self._call(
            OPERATIONS["get_billing_plans"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_bootstrap(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /bootstrap"""
        return await self._call(
            OPERATIONS["get_bootstrap"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_buckets_by_bucket_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /buckets/{bucketId}"""
        return await self._call(
            OPERATIONS["get_buckets_by_bucket_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_buckets_by_bucket_id_files(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /buckets/{bucketId}/files"""
        return await self._call(
            OPERATIONS["get_buckets_by_bucket_id_files"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_buckets_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /buckets/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_buckets_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_cms_careers(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /cms/careers"""
        return await self._call(
            OPERATIONS["get_cms_careers"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_cms_faqs_by_page_slug(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /cms/faqs/{pageSlug}"""
        return await self._call(
            OPERATIONS["get_cms_faqs_by_page_slug"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_cms_pages_by_slug(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /cms/pages/{slug}"""
        return await self._call(
            OPERATIONS["get_cms_pages_by_slug"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_cms_partners(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /cms/partners"""
        return await self._call(
            OPERATIONS["get_cms_partners"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_cms_team(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /cms/team"""
        return await self._call(
            OPERATIONS["get_cms_team"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_cms_testimonials(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /cms/testimonials"""
        return await self._call(
            OPERATIONS["get_cms_testimonials"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_credits_org_by_org_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /credits/org/{orgId}"""
        return await self._call(
            OPERATIONS["get_credits_org_by_org_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_credits_org_by_org_id_balance(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /credits/org/{orgId}/balance"""
        return await self._call(
            OPERATIONS["get_credits_org_by_org_id_balance"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_database_connector_by_project_id_tables(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /database/connector/{projectId}/tables"""
        return await self._call(
            OPERATIONS["get_database_connector_by_project_id_tables"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_database_extensions_available(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /database/extensions/available"""
        return await self._call(
            OPERATIONS["get_database_extensions_available"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_database_extensions_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /database/extensions/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_database_extensions_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_database_tiers(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /database/tiers"""
        return await self._call(
            OPERATIONS["get_database_tiers"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_database_wrappers_available(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /database/wrappers/available"""
        return await self._call(
            OPERATIONS["get_database_wrappers_available"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_database_wrappers_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /database/wrappers/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_database_wrappers_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_deployments_by_deployment_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /deployments/{deploymentId}"""
        return await self._call(
            OPERATIONS["get_deployments_by_deployment_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_deployments_by_deployment_id_steps(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /deployments/{deploymentId}/steps"""
        return await self._call(
            OPERATIONS["get_deployments_by_deployment_id_steps"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_deployments_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /deployments/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_deployments_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_deployments_project_by_project_id_stats(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /deployments/project/{projectId}/stats"""
        return await self._call(
            OPERATIONS["get_deployments_project_by_project_id_stats"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_deployments_tokens_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /deployments/tokens/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_deployments_tokens_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_docs_ai_search(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/ai-search"""
        return await self._call(
            OPERATIONS["get_docs_ai_search"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_docs_api_endpoints(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/api-endpoints"""
        return await self._call(
            OPERATIONS["get_docs_api_endpoints"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_docs_api_endpoints_by_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/api-endpoints/{id}"""
        return await self._call(
            OPERATIONS["get_docs_api_endpoints_by_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_docs_categories(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/categories"""
        return await self._call(
            OPERATIONS["get_docs_categories"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_docs_changelog(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/changelog"""
        return await self._call(
            OPERATIONS["get_docs_changelog"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_docs_changelog_by_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/changelog/{id}"""
        return await self._call(
            OPERATIONS["get_docs_changelog_by_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_docs_examples(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/examples"""
        return await self._call(
            OPERATIONS["get_docs_examples"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_docs_examples_by_slug(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/examples/{slug}"""
        return await self._call(
            OPERATIONS["get_docs_examples_by_slug"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_docs_project_by_project_id_quickstart(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/project/{projectId}/quickstart"""
        return await self._call(
            OPERATIONS["get_docs_project_by_project_id_quickstart"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_docs_sdks(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/sdks"""
        return await self._call(
            OPERATIONS["get_docs_sdks"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_docs_sdks_by_platform(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/sdks/{platform}"""
        return await self._call(
            OPERATIONS["get_docs_sdks_by_platform"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_docs_sdks_by_sdk_id_examples(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/sdks/{sdkId}/examples"""
        return await self._call(
            OPERATIONS["get_docs_sdks_by_sdk_id_examples"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_docs_search(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/search"""
        return await self._call(
            OPERATIONS["get_docs_search"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_docs_v2_pages(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/v2/pages"""
        return await self._call(
            OPERATIONS["get_docs_v2_pages"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_docs_v2_pages_by_slug(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /docs/v2/pages/{slug}"""
        return await self._call(
            OPERATIONS["get_docs_v2_pages_by_slug"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_early_by_number(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /early/{number}"""
        return await self._call(
            OPERATIONS["get_early_by_number"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_early_wall(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /early/wall"""
        return await self._call(
            OPERATIONS["get_early_wall"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_enterprise_org_by_org_id_contract(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /enterprise/org/{orgId}/contract"""
        return await self._call(
            OPERATIONS["get_enterprise_org_by_org_id_contract"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_enterprise_org_by_org_id_invoices(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /enterprise/org/{orgId}/invoices"""
        return await self._call(
            OPERATIONS["get_enterprise_org_by_org_id_invoices"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_enterprise_org_by_org_id_onboarding(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /enterprise/org/{orgId}/onboarding"""
        return await self._call(
            OPERATIONS["get_enterprise_org_by_org_id_onboarding"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_enterprise_org_by_org_id_spend(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /enterprise/org/{orgId}/spend"""
        return await self._call(
            OPERATIONS["get_enterprise_org_by_org_id_spend"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_enterprise_org_by_org_id_usage(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /enterprise/org/{orgId}/usage"""
        return await self._call(
            OPERATIONS["get_enterprise_org_by_org_id_usage"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_enterprise_org_by_org_id_usage_history(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /enterprise/org/{orgId}/usage/history"""
        return await self._call(
            OPERATIONS["get_enterprise_org_by_org_id_usage_history"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_enterprise_org_by_org_id_usage_projects(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /enterprise/org/{orgId}/usage/projects"""
        return await self._call(
            OPERATIONS["get_enterprise_org_by_org_id_usage_projects"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_enterprise_pricing(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /enterprise/pricing"""
        return await self._call(
            OPERATIONS["get_enterprise_pricing"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_enterprise_quotes_by_quote_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /enterprise/quotes/{quoteId}"""
        return await self._call(
            OPERATIONS["get_enterprise_quotes_by_quote_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_entitlements_org_by_org_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /entitlements/org/{orgId}"""
        return await self._call(
            OPERATIONS["get_entitlements_org_by_org_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_functions_by_function_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /functions/{functionId}"""
        return await self._call(
            OPERATIONS["get_functions_by_function_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_functions_by_function_id_deploy_status(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /functions/{functionId}/deploy-status"""
        return await self._call(
            OPERATIONS["get_functions_by_function_id_deploy_status"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_functions_by_function_id_invocations(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /functions/{functionId}/invocations"""
        return await self._call(
            OPERATIONS["get_functions_by_function_id_invocations"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_functions_by_function_id_logs(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /functions/{functionId}/logs"""
        return await self._call(
            OPERATIONS["get_functions_by_function_id_logs"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_functions_by_function_id_metrics(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /functions/{functionId}/metrics"""
        return await self._call(
            OPERATIONS["get_functions_by_function_id_metrics"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_functions_by_function_id_schedule(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /functions/{functionId}/schedule"""
        return await self._call(
            OPERATIONS["get_functions_by_function_id_schedule"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_functions_by_function_id_triggers(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /functions/{functionId}/triggers"""
        return await self._call(
            OPERATIONS["get_functions_by_function_id_triggers"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_functions_invocations(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /functions/invocations"""
        return await self._call(
            OPERATIONS["get_functions_invocations"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_functions_invocations_function_by_function_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /functions/invocations/function/{functionId}"""
        return await self._call(
            OPERATIONS["get_functions_invocations_function_by_function_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_functions_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /functions/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_functions_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_functions_project_by_project_id_name_by_function_name(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /functions/project/{projectId}/name/{functionName}"""
        return await self._call(
            OPERATIONS["get_functions_project_by_project_id_name_by_function_name"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_functions_project_by_project_id_summary(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /functions/project/{projectId}/summary"""
        return await self._call(
            OPERATIONS["get_functions_project_by_project_id_summary"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_functions_schedule_preview(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /functions/schedule/preview"""
        return await self._call(
            OPERATIONS["get_functions_schedule_preview"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_functions_secrets_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /functions/secrets/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_functions_secrets_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_generated_by_table(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /generated/{table}"""
        return await self._call(
            OPERATIONS["get_generated_by_table"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_generated_by_table_aggregate(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /generated/{table}/aggregate"""
        return await self._call(
            OPERATIONS["get_generated_by_table_aggregate"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_generated_by_table_by_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /generated/{table}/{id}"""
        return await self._call(
            OPERATIONS["get_generated_by_table_by_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_generated_by_table_search(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /generated/{table}/search"""
        return await self._call(
            OPERATIONS["get_generated_by_table_search"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_github_oauth_authorize(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /github/oauth/authorize"""
        return await self._call(
            OPERATIONS["get_github_oauth_authorize"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_incidents_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /incidents/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_incidents_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_infrastructure_sizes(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /infrastructure/sizes"""
        return await self._call(
            OPERATIONS["get_infrastructure_sizes"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_integrations_analytics_project_by_project_id_events(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /integrations/analytics/project/{projectId}/events"""
        return await self._call(
            OPERATIONS["get_integrations_analytics_project_by_project_id_events"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_integrations_analytics_project_by_project_id_stats(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /integrations/analytics/project/{projectId}/stats"""
        return await self._call(
            OPERATIONS["get_integrations_analytics_project_by_project_id_stats"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_integrations_deliveries_event_by_event_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /integrations/deliveries/event/{eventId}"""
        return await self._call(
            OPERATIONS["get_integrations_deliveries_event_by_event_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_integrations_deliveries_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /integrations/deliveries/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_integrations_deliveries_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_integrations_deliveries_project_by_project_id_summary(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /integrations/deliveries/project/{projectId}/summary"""
        return await self._call(
            OPERATIONS["get_integrations_deliveries_project_by_project_id_summary"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_integrations_deliveries_subscription_by_subscription_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /integrations/deliveries/subscription/{subscriptionId}"""
        return await self._call(
            OPERATIONS["get_integrations_deliveries_subscription_by_subscription_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_integrations_dlq_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /integrations/dlq/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_integrations_dlq_project_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_integrations_events(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /integrations/events"""
        return await self._call(
            OPERATIONS["get_integrations_events"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_integrations_subscriptions_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /integrations/subscriptions/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_integrations_subscriptions_project_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_jobs_dlq_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /jobs/dlq/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_jobs_dlq_project_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_jobs_webhooks_delivery_by_delivery_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /jobs/webhooks/delivery/{deliveryId}"""
        return await self._call(
            OPERATIONS["get_jobs_webhooks_delivery_by_delivery_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_jobs_webhooks_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /jobs/webhooks/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_jobs_webhooks_project_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_logs_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /logs/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_logs_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_logs_project_by_project_id_feed(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /logs/project/{projectId}/feed"""
        return await self._call(
            OPERATIONS["get_logs_project_by_project_id_feed"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_maintenance(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /maintenance"""
        return await self._call(
            OPERATIONS["get_maintenance"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_mcp_connections(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /mcp/connections"""
        return await self._call(
            OPERATIONS["get_mcp_connections"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_mcp_oauth_requests_by_request_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /mcp/oauth/requests/{requestId}"""
        return await self._call(
            OPERATIONS["get_mcp_oauth_requests_by_request_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_mcp_session(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /mcp/session"""
        return await self._call(
            OPERATIONS["get_mcp_session"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_me_badges(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /me/badges"""
        return await self._call(
            OPERATIONS["get_me_badges"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_me_creator(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /me/creator"""
        return await self._call(
            OPERATIONS["get_me_creator"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_metrics_org_by_org_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /metrics/org/{orgId}"""
        return await self._call(
            OPERATIONS["get_metrics_org_by_org_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_metrics_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /metrics/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_metrics_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_metrics_project_by_project_id_overview(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /metrics/project/{projectId}/overview"""
        return await self._call(
            OPERATIONS["get_metrics_project_by_project_id_overview"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_metrics_project_by_project_id_report(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /metrics/project/{projectId}/report"""
        return await self._call(
            OPERATIONS["get_metrics_project_by_project_id_report"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_mongodb_by_collection_estimated_count(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /mongodb/{collection}/estimatedCount"""
        return await self._call(
            OPERATIONS["get_mongodb_by_collection_estimated_count"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_mongodb_by_collection_find_by_id_by_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /mongodb/{collection}/findById/{id}"""
        return await self._call(
            OPERATIONS["get_mongodb_by_collection_find_by_id_by_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_mongodb_by_collection_indexes(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /mongodb/{collection}/indexes"""
        return await self._call(
            OPERATIONS["get_mongodb_by_collection_indexes"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_mongodb_collections(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /mongodb/collections"""
        return await self._call(
            OPERATIONS["get_mongodb_collections"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_oauth_org_by_org_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /oauth/org/{orgId}"""
        return await self._call(
            OPERATIONS["get_oauth_org_by_org_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_oauth_org_by_org_id_provider_by_provider_authorize(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /oauth/org/{orgId}/provider/{provider}/authorize"""
        return await self._call(
            OPERATIONS["get_oauth_org_by_org_id_provider_by_provider_authorize"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_onboarding_org_by_org_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /onboarding/org/{orgId}"""
        return await self._call(
            OPERATIONS["get_onboarding_org_by_org_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_openapi_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /openapi/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_openapi_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_openapi_yaml(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /openapi.yaml"""
        return await self._call(
            OPERATIONS["get_openapi_yaml"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs"""
        return await self._call(
            OPERATIONS["get_orgs"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_access_matrix(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/access-matrix"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_access_matrix"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_blueprint_defaults(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/blueprint-defaults"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_blueprint_defaults"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_change_requests(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/change-requests"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_change_requests"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_data_region(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/data-region"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_data_region"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_identity_summary(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/identity/summary"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_identity_summary"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_invites(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/invites"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_invites"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_leave_requests(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/leave-requests"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_leave_requests"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_leave_requests_mine(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/leave-requests/mine"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_leave_requests_mine"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_managed_domains(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/managed-domains"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_managed_domains"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_managed_summary(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/managed-summary"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_managed_summary"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_members(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/members"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_members"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_membership(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/membership"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_membership"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_profile(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/profile"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_profile"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_roles(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/roles"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_roles"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_security(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/security"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_security"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_security_posture(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/security/posture"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_security_posture"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_support_sla_report(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/support/sla-report"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_support_sla_report"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_support_summary(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/support/summary"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_support_summary"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_support_terms(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/support/terms"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_support_terms"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_support_tickets(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/support/tickets"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_support_tickets"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_support_tickets_by_number(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/support/tickets/{number}"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_support_tickets_by_number"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_by_org_id_transfers(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/{orgId}/transfers"""
        return await self._call(
            OPERATIONS["get_orgs_by_org_id_transfers"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_orgs_invites_lookup(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/invites/lookup"""
        return await self._call(
            OPERATIONS["get_orgs_invites_lookup"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_orgs_transfers_preview(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /orgs/transfers/preview"""
        return await self._call(
            OPERATIONS["get_orgs_transfers_preview"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_plans_by_plan_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /plans/{planId}"""
        return await self._call(
            OPERATIONS["get_plans_by_plan_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_plans_org_by_org_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /plans/org/{orgId}"""
        return await self._call(
            OPERATIONS["get_plans_org_by_org_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_pricing_ai_features(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /pricing/ai-features"""
        return await self._call(
            OPERATIONS["get_pricing_ai_features"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_pricing_compare(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /pricing/compare"""
        return await self._call(
            OPERATIONS["get_pricing_compare"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_pricing_enterprise(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /pricing/enterprise"""
        return await self._call(
            OPERATIONS["get_pricing_enterprise"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_pricing_plans(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /pricing/plans"""
        return await self._call(
            OPERATIONS["get_pricing_plans"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_pricing_plans_by_plan(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /pricing/plans/{plan}"""
        return await self._call(
            OPERATIONS["get_pricing_plans_by_plan"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects"""
        return await self._call(
            OPERATIONS["get_projects"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_projects_by_id_insights(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{id}/insights"""
        return await self._call(
            OPERATIONS["get_projects_by_id_insights"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_api_keys(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/api-keys"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_api_keys"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_auth_activity(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/auth/activity"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_auth_activity"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_auth_me(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/auth/me"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_auth_me"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_auth_oauth_apps(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/auth/oauth-apps"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_auth_oauth_apps"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_auth_oauth_providers(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/auth/oauth/providers"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_auth_oauth_providers"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_auth_sessions(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/auth/sessions"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_auth_sessions"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_auth_settings(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/auth/settings"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_auth_settings"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_branches(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/branches"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_branches"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_branches_by_branch_name_url(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/branches/{branchName}/url"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_branches_by_branch_name_url"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_database_dedicated(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/database/dedicated"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_database_dedicated"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_database_dedicated_connection(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/database/dedicated/connection"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_database_dedicated_connection"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_database_dedicated_status(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/database/dedicated/status"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_database_dedicated_status"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_deletion_preview(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/deletion-preview"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_deletion_preview"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_env_vars(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/env-vars"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_env_vars"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_environments(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/environments"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_environments"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_environments_by_env_id_domain_status(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/environments/{envId}/domain-status"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_environments_by_env_id_domain_status"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_environments_by_env_id_domain_verification(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/environments/{envId}/domain-verification"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_environments_by_env_id_domain_verification"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_environments_by_env_id_domains(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/environments/{envId}/domains"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_environments_by_env_id_domains"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_environments_promotion_order(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/environments/promotion-order"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_environments_promotion_order"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_frontend(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/frontend"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_frontend"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_getting_started(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/getting-started"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_getting_started"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_github_branches(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/github/branches"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_github_branches"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_github_repos(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/github/repos"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_github_repos"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_github_status(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/github/status"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_github_status"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_github_tracked_repos(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/github/tracked-repos"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_github_tracked_repos"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_infrastructure(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/infrastructure"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_infrastructure"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_infrastructure_by_instance_id_metrics(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/infrastructure/{instanceId}/metrics"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_infrastructure_by_instance_id_metrics"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_infrastructure_by_instance_id_replicas(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/infrastructure/{instanceId}/replicas"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_infrastructure_by_instance_id_replicas"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_infrastructure_by_instance_id_upgrade_options(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/infrastructure/{instanceId}/upgrade-options"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_infrastructure_by_instance_id_upgrade_options"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_infrastructure_migration_progress(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/infrastructure/migration/progress"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_infrastructure_migration_progress"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_infrastructure_migration_status(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/infrastructure/migration-status"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_infrastructure_migration_status"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_infrastructure_restores(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/infrastructure/restores"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_infrastructure_restores"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_members(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/members"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_members"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_promotions(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/promotions"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_promotions"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_promotions_diff(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/promotions/diff"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_promotions_diff"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_region(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/region"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_region"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_security_advisor(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/security/advisor"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_security_advisor"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_settings(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/settings"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_settings"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_settings_addons(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/settings/addons"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_settings_addons"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_settings_api(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/settings/api"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_settings_api"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_settings_compute(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/settings/compute"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_settings_compute"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_settings_jwt(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/settings/jwt"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_settings_jwt"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_storage_settings(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/storage/settings"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_storage_settings"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_users(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/users"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_users"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_users_by_user_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/users/{userId}"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_users_by_user_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_users_by_user_id_sessions(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/users/{userId}/sessions"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_users_by_user_id_sessions"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_by_project_id_users_stats(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/{projectId}/users/stats"""
        return await self._call(
            OPERATIONS["get_projects_by_project_id_users_stats"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_projects_slug_available(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /projects/slug-available"""
        return await self._call(
            OPERATIONS["get_projects_slug_available"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_quickstart_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /quickstart/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_quickstart_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_quickstart_project_by_project_id_json(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /quickstart/project/{projectId}/json"""
        return await self._call(
            OPERATIONS["get_quickstart_project_by_project_id_json"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_realtime_connections_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /realtime/connections/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_realtime_connections_project_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_realtime_events_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /realtime/events/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_realtime_events_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_realtime_stats_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /realtime/stats/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_realtime_stats_project_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_realtime_status_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /realtime/status/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_realtime_status_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_realtime_subscriptions_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /realtime/subscriptions/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_realtime_subscriptions_project_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_refunds_by_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /refunds/{id}"""
        return await self._call(
            OPERATIONS["get_refunds_by_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_refunds_org_by_org_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /refunds/org/{orgId}"""
        return await self._call(
            OPERATIONS["get_refunds_org_by_org_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_regions(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /regions"""
        return await self._call(
            OPERATIONS["get_regions"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_regions_all(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /regions/all"""
        return await self._call(
            OPERATIONS["get_regions_all"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_regions_by_key(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /regions/{key}"""
        return await self._call(
            OPERATIONS["get_regions_by_key"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_regions_by_key_metrics(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /regions/{key}/metrics"""
        return await self._call(
            OPERATIONS["get_regions_by_key_metrics"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_regions_health(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /regions/health"""
        return await self._call(
            OPERATIONS["get_regions_health"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_rls_policies_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /rls/policies/{projectId}"""
        return await self._call(
            OPERATIONS["get_rls_policies_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_schema_engine_by_project_id_changes(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /schema-engine/{projectId}/changes"""
        return await self._call(
            OPERATIONS["get_schema_engine_by_project_id_changes"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_schema_engine_editor_sessions_by_project_id_capabilities(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /schema-engine/editor-sessions/{projectId}/capabilities"""
        return await self._call(
            OPERATIONS["get_schema_engine_editor_sessions_by_project_id_capabilities"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_schema_engine_introspect_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /schema-engine/introspect/{projectId}"""
        return await self._call(
            OPERATIONS["get_schema_engine_introspect_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_schema_engine_migrations_by_project_id_by_migration_id_diff(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /schema-engine/migrations/{projectId}/{migrationId}/diff"""
        return await self._call(
            OPERATIONS["get_schema_engine_migrations_by_project_id_by_migration_id_diff"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_schema_engine_migrations_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /schema-engine/migrations/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_schema_engine_migrations_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_schema_engine_snapshots_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /schema-engine/snapshots/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_schema_engine_snapshots_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_schema_engine_snippets_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /schema-engine/snippets/{projectId}"""
        return await self._call(
            OPERATIONS["get_schema_engine_snippets_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_schemas_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /schemas/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_schemas_project_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_security_audit_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /security/audit/{projectId}"""
        return await self._call(
            OPERATIONS["get_security_audit_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_security_overview_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /security/overview/{projectId}"""
        return await self._call(
            OPERATIONS["get_security_overview_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_security_variables_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /security/variables/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_security_variables_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_services_by_service_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /services/{serviceId}"""
        return await self._call(
            OPERATIONS["get_services_by_service_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_services_by_service_id_deployments_by_deployment_id_build_logs(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /services/{serviceId}/deployments/{deploymentId}/build-logs"""
        return await self._call(
            OPERATIONS["get_services_by_service_id_deployments_by_deployment_id_build_logs"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_services_by_service_id_deployments_by_deployment_id_status(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /services/{serviceId}/deployments/{deploymentId}/status"""
        return await self._call(
            OPERATIONS["get_services_by_service_id_deployments_by_deployment_id_status"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_services_by_service_id_domains(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /services/{serviceId}/domains"""
        return await self._call(
            OPERATIONS["get_services_by_service_id_domains"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_services_by_service_id_git_connect(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /services/{serviceId}/git/connect"""
        return await self._call(
            OPERATIONS["get_services_by_service_id_git_connect"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_services_by_service_id_logs(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /services/{serviceId}/logs"""
        return await self._call(
            OPERATIONS["get_services_by_service_id_logs"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_services_by_service_id_status(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /services/{serviceId}/status"""
        return await self._call(
            OPERATIONS["get_services_by_service_id_status"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_services_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /services/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_services_project_by_project_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_services_project_by_project_id_summary(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /services/project/{projectId}/summary"""
        return await self._call(
            OPERATIONS["get_services_project_by_project_id_summary"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_sso_me_paused_access(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /sso/me/paused-access"""
        return await self._call(
            OPERATIONS["get_sso_me_paused_access"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_sso_org_by_org_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /sso/org/{orgId}"""
        return await self._call(
            OPERATIONS["get_sso_org_by_org_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_sso_org_by_org_id_connections_by_connection_id_break_glass(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /sso/org/{orgId}/connections/{connectionId}/break-glass"""
        return await self._call(
            OPERATIONS["get_sso_org_by_org_id_connections_by_connection_id_break_glass"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_sso_org_by_org_id_connections_by_connection_id_certificates(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /sso/org/{orgId}/connections/{connectionId}/certificates"""
        return await self._call(
            OPERATIONS["get_sso_org_by_org_id_connections_by_connection_id_certificates"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_sso_org_by_org_id_connections_by_connection_id_group_mappings(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /sso/org/{orgId}/connections/{connectionId}/group-mappings"""
        return await self._call(
            OPERATIONS["get_sso_org_by_org_id_connections_by_connection_id_group_mappings"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_sso_org_by_org_id_connections_by_connection_id_require(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /sso/org/{orgId}/connections/{connectionId}/require"""
        return await self._call(
            OPERATIONS["get_sso_org_by_org_id_connections_by_connection_id_require"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_sso_org_by_org_id_connections_by_connection_id_scim_reconciliation(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /sso/org/{orgId}/connections/{connectionId}/scim/reconciliation"""
        return await self._call(
            OPERATIONS["get_sso_org_by_org_id_connections_by_connection_id_scim_reconciliation"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_sso_org_by_org_id_connections_by_connection_id_scim_tokens(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /sso/org/{orgId}/connections/{connectionId}/scim/tokens"""
        return await self._call(
            OPERATIONS["get_sso_org_by_org_id_connections_by_connection_id_scim_tokens"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_sso_org_by_org_id_outside_members(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /sso/org/{orgId}/outside-members"""
        return await self._call(
            OPERATIONS["get_sso_org_by_org_id_outside_members"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_sso_org_by_org_id_outside_members_blocked(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /sso/org/{orgId}/outside-members/blocked"""
        return await self._call(
            OPERATIONS["get_sso_org_by_org_id_outside_members_blocked"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_sso_org_by_org_id_security_contact(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /sso/org/{orgId}/security-contact"""
        return await self._call(
            OPERATIONS["get_sso_org_by_org_id_security_contact"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_status(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /status"""
        return await self._call(
            OPERATIONS["get_status"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_status_atom(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /status/atom"""
        return await self._call(
            OPERATIONS["get_status_atom"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_status_incidents(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /status/incidents"""
        return await self._call(
            OPERATIONS["get_status_incidents"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_status_rss(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /status/rss"""
        return await self._call(
            OPERATIONS["get_status_rss"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_status_subscribers_count(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /status/subscribers/count"""
        return await self._call(
            OPERATIONS["get_status_subscribers_count"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_status_unsubscribe_by_token(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /status/unsubscribe/{token}"""
        return await self._call(
            OPERATIONS["get_status_unsubscribe_by_token"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_status_uptime_by_component_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /status/uptime/{componentId}"""
        return await self._call(
            OPERATIONS["get_status_uptime_by_component_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_storage_buckets(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /storage/buckets"""
        return await self._call(
            OPERATIONS["get_storage_buckets"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_storage_buckets_by_bucket_id_policies(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /storage/buckets/{bucketId}/policies"""
        return await self._call(
            OPERATIONS["get_storage_buckets_by_bucket_id_policies"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_storage_download(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> bytes:
        """GET /storage/download"""
        return cast(
            bytes,
            await self._call(
                OPERATIONS["get_storage_download"],
                path=None,
                query=query,
                body=None,
                headers=headers,
            ),
        )

    async def get_storage_files_by_bucket_id_metadata(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /storage/files/{bucketId}/metadata"""
        return await self._call(
            OPERATIONS["get_storage_files_by_bucket_id_metadata"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_storage_multipart_list_pending(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /storage/multipart/list-pending"""
        return await self._call(
            OPERATIONS["get_storage_multipart_list_pending"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_storage_usage_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /storage/usage/project/{projectId}"""
        return await self._call(
            OPERATIONS["get_storage_usage_project_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_templates(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /templates"""
        return await self._call(
            OPERATIONS["get_templates"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_templates_by_slug(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /templates/{slug}"""
        return await self._call(
            OPERATIONS["get_templates_by_slug"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_templates_installs(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /templates/installs"""
        return await self._call(
            OPERATIONS["get_templates_installs"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_tenant_branding(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /tenant/branding"""
        return await self._call(
            OPERATIONS["get_tenant_branding"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_users_me(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /users/me"""
        return await self._call(
            OPERATIONS["get_users_me"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_users_me_preferences(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /users/me/preferences"""
        return await self._call(
            OPERATIONS["get_users_me_preferences"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_v1_data_by_project_id_by_table(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /v1/data/{projectId}/{table}"""
        return await self._call(
            OPERATIONS["get_v1_data_by_project_id_by_table"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_v1_data_by_project_id_by_table_aggregate(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /v1/data/{projectId}/{table}/aggregate"""
        return await self._call(
            OPERATIONS["get_v1_data_by_project_id_by_table_aggregate"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_v1_data_by_project_id_by_table_by_id(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /v1/data/{projectId}/{table}/{id}"""
        return await self._call(
            OPERATIONS["get_v1_data_by_project_id_by_table_by_id"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_v1_data_by_project_id_by_table_search(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /v1/data/{projectId}/{table}/search"""
        return await self._call(
            OPERATIONS["get_v1_data_by_project_id_by_table_search"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def get_v1_health(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /v1/health"""
        return await self._call(
            OPERATIONS["get_v1_health"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_v1_project(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /v1/project"""
        return await self._call(
            OPERATIONS["get_v1_project"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def get_well_known_oauth_authorization_server(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """GET /.well-known/oauth-authorization-server"""
        return await self._call(
            OPERATIONS["get_well_known_oauth_authorization_server"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def patch_ai_copilot_session_by_session_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /ai/copilot/session/{sessionId}"""
        return await self._call(
            OPERATIONS["patch_ai_copilot_session_by_session_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_auth_me(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /auth/me"""
        return await self._call(
            OPERATIONS["patch_auth_me"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_billing_org_by_org_id_addons_by_addon_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /billing/org/{orgId}/addons/{addonId}"""
        return await self._call(
            OPERATIONS["patch_billing_org_by_org_id_addons_by_addon_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_billing_org_by_org_id_contacts_by_contact_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /billing/org/{orgId}/contacts/{contactId}"""
        return await self._call(
            OPERATIONS["patch_billing_org_by_org_id_contacts_by_contact_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_billing_org_by_org_id_usage_alerts_by_alert_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /billing/org/{orgId}/usage-alerts/{alertId}"""
        return await self._call(
            OPERATIONS["patch_billing_org_by_org_id_usage_alerts_by_alert_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_database_wrappers_project_by_project_id_by_wrapper_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /database/wrappers/project/{projectId}/{wrapperId}"""
        return await self._call(
            OPERATIONS["patch_database_wrappers_project_by_project_id_by_wrapper_id"],
            path=path,
            query=query,
            body=body,
            headers=headers,
        )

    async def patch_enterprise_org_by_org_id_onboarding(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /enterprise/org/{orgId}/onboarding"""
        return await self._call(
            OPERATIONS["patch_enterprise_org_by_org_id_onboarding"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_functions_by_function_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /functions/{functionId}"""
        return await self._call(
            OPERATIONS["patch_functions_by_function_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_functions_triggers_by_trigger_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /functions/triggers/{triggerId}"""
        return await self._call(
            OPERATIONS["patch_functions_triggers_by_trigger_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_generated_by_table_bulk(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /generated/{table}/bulk"""
        return await self._call(
            OPERATIONS["patch_generated_by_table_bulk"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_generated_by_table_by_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /generated/{table}/{id}"""
        return await self._call(
            OPERATIONS["patch_generated_by_table_by_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_integrations_subscriptions_by_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /integrations/subscriptions/{id}"""
        return await self._call(
            OPERATIONS["patch_integrations_subscriptions_by_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_oauth_org_by_org_id_provider_by_provider(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /oauth/org/{orgId}/provider/{provider}"""
        return await self._call(
            OPERATIONS["patch_oauth_org_by_org_id_provider_by_provider"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_orgs_by_org_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /orgs/{orgId}"""
        return await self._call(
            OPERATIONS["patch_orgs_by_org_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_orgs_by_org_id_blueprint_defaults(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /orgs/{orgId}/blueprint-defaults"""
        return await self._call(
            OPERATIONS["patch_orgs_by_org_id_blueprint_defaults"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_orgs_by_org_id_data_region(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /orgs/{orgId}/data-region"""
        return await self._call(
            OPERATIONS["patch_orgs_by_org_id_data_region"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_orgs_by_org_id_members_by_user_id_role(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /orgs/{orgId}/members/{userId}/role"""
        return await self._call(
            OPERATIONS["patch_orgs_by_org_id_members_by_user_id_role"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_orgs_by_org_id_members_roles(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /orgs/{orgId}/members/roles"""
        return await self._call(
            OPERATIONS["patch_orgs_by_org_id_members_roles"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_orgs_by_org_id_profile(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /orgs/{orgId}/profile"""
        return await self._call(
            OPERATIONS["patch_orgs_by_org_id_profile"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_orgs_by_org_id_security(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /orgs/{orgId}/security"""
        return await self._call(
            OPERATIONS["patch_orgs_by_org_id_security"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_projects_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /projects/{projectId}"""
        return await self._call(
            OPERATIONS["patch_projects_by_project_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_projects_by_project_id_api_keys_by_key_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /projects/{projectId}/api-keys/{keyId}"""
        return await self._call(
            OPERATIONS["patch_projects_by_project_id_api_keys_by_key_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_projects_by_project_id_auth_settings(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /projects/{projectId}/auth/settings"""
        return await self._call(
            OPERATIONS["patch_projects_by_project_id_auth_settings"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_projects_by_project_id_env_vars_by_env_var_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /projects/{projectId}/env-vars/{envVarId}"""
        return await self._call(
            OPERATIONS["patch_projects_by_project_id_env_vars_by_env_var_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_projects_by_project_id_environments_by_env_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /projects/{projectId}/environments/{envId}"""
        return await self._call(
            OPERATIONS["patch_projects_by_project_id_environments_by_env_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_projects_by_project_id_settings_addons(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /projects/{projectId}/settings/addons"""
        return await self._call(
            OPERATIONS["patch_projects_by_project_id_settings_addons"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_projects_by_project_id_settings_api(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /projects/{projectId}/settings/api"""
        return await self._call(
            OPERATIONS["patch_projects_by_project_id_settings_api"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_projects_by_project_id_settings_compute(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /projects/{projectId}/settings/compute"""
        return await self._call(
            OPERATIONS["patch_projects_by_project_id_settings_compute"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_projects_by_project_id_settings_jwt(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /projects/{projectId}/settings/jwt"""
        return await self._call(
            OPERATIONS["patch_projects_by_project_id_settings_jwt"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_projects_by_project_id_storage_settings(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /projects/{projectId}/storage/settings"""
        return await self._call(
            OPERATIONS["patch_projects_by_project_id_storage_settings"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_projects_by_project_id_users_by_user_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /projects/{projectId}/users/{userId}"""
        return await self._call(
            OPERATIONS["patch_projects_by_project_id_users_by_user_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_regions_by_key(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /regions/{key}"""
        return await self._call(
            OPERATIONS["patch_regions_by_key"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_rls_policies_by_policy_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /rls/policies/{policyId}"""
        return await self._call(
            OPERATIONS["patch_rls_policies_by_policy_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_schema_engine_snippets_by_project_id_by_snippet_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /schema-engine/snippets/{projectId}/{snippetId}"""
        return await self._call(
            OPERATIONS["patch_schema_engine_snippets_by_project_id_by_snippet_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_services_by_service_id_hostname(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /services/{serviceId}/hostname"""
        return await self._call(
            OPERATIONS["patch_services_by_service_id_hostname"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_services_by_service_id_runtime_class(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /services/{serviceId}/runtime-class"""
        return await self._call(
            OPERATIONS["patch_services_by_service_id_runtime_class"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_sso_org_by_org_id_connections_by_connection_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /sso/org/{orgId}/connections/{connectionId}"""
        return await self._call(
            OPERATIONS["patch_sso_org_by_org_id_connections_by_connection_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_storage_files_by_bucket_id_metadata(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /storage/files/{bucketId}/metadata"""
        return await self._call(
            OPERATIONS["patch_storage_files_by_bucket_id_metadata"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_users_me(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /users/me"""
        return await self._call(
            OPERATIONS["patch_users_me"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_users_me_preferences(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /users/me/preferences"""
        return await self._call(
            OPERATIONS["patch_users_me_preferences"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_v1_data_by_project_id_by_table_bulk(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /v1/data/{projectId}/{table}/bulk"""
        return await self._call(
            OPERATIONS["patch_v1_data_by_project_id_by_table_bulk"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def patch_v1_data_by_project_id_by_table_by_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PATCH /v1/data/{projectId}/{table}/{id}"""
        return await self._call(
            OPERATIONS["patch_v1_data_by_project_id_by_table_by_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_alert_rule_suggestion(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/alert-rule-suggestion"""
        return await self._call(
            OPERATIONS["post_ai_copilot_alert_rule_suggestion"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_alert_rule_suggestion_estimate(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/alert-rule-suggestion/estimate"""
        return await self._call(
            OPERATIONS["post_ai_copilot_alert_rule_suggestion_estimate"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_chat(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/chat"""
        return await self._call(
            OPERATIONS["post_ai_copilot_chat"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_chat_stream(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/chat/stream"""
        return await self._call(
            OPERATIONS["post_ai_copilot_chat_stream"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_ai_copilot_execute(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/execute"""
        return await self._call(
            OPERATIONS["post_ai_copilot_execute"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_execution_by_execution_id_pause(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/execution/{executionId}/pause"""
        return await self._call(
            OPERATIONS["post_ai_copilot_execution_by_execution_id_pause"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_ai_copilot_execution_by_execution_id_resume(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/execution/{executionId}/resume"""
        return await self._call(
            OPERATIONS["post_ai_copilot_execution_by_execution_id_resume"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_execution_by_execution_id_rollback(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/execution/{executionId}/rollback"""
        return await self._call(
            OPERATIONS["post_ai_copilot_execution_by_execution_id_rollback"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_export_by_version_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/export/{versionId}"""
        return await self._call(
            OPERATIONS["post_ai_copilot_export_by_version_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_export_github(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/export/github"""
        return await self._call(
            OPERATIONS["post_ai_copilot_export_github"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_feedback(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/feedback"""
        return await self._call(
            OPERATIONS["post_ai_copilot_feedback"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_generation_by_manifest_id_cancel(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/generation/{manifestId}/cancel"""
        return await self._call(
            OPERATIONS["post_ai_copilot_generation_by_manifest_id_cancel"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_git_branch(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/git/branch"""
        return await self._call(
            OPERATIONS["post_ai_copilot_git_branch"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_git_clone(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/git/clone"""
        return await self._call(
            OPERATIONS["post_ai_copilot_git_clone"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_git_commit(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/git/commit"""
        return await self._call(
            OPERATIONS["post_ai_copilot_git_commit"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_git_init(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/git/init"""
        return await self._call(
            OPERATIONS["post_ai_copilot_git_init"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_git_pull(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/git/pull"""
        return await self._call(
            OPERATIONS["post_ai_copilot_git_pull"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_git_push(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/git/push"""
        return await self._call(
            OPERATIONS["post_ai_copilot_git_push"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_git_write(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/git/write"""
        return await self._call(
            OPERATIONS["post_ai_copilot_git_write"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_job(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/job"""
        return await self._call(
            OPERATIONS["post_ai_copilot_job"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_job_by_job_id_cancel(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/job/{jobId}/cancel"""
        return await self._call(
            OPERATIONS["post_ai_copilot_job_by_job_id_cancel"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_ai_copilot_job_by_job_id_retry(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/job/{jobId}/retry"""
        return await self._call(
            OPERATIONS["post_ai_copilot_job_by_job_id_retry"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_manifest_by_manifest_id_pause(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/manifest/{manifestId}/pause"""
        return await self._call(
            OPERATIONS["post_ai_copilot_manifest_by_manifest_id_pause"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_memories_by_memory_id_promote(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/memories/{memoryId}/promote"""
        return await self._call(
            OPERATIONS["post_ai_copilot_memories_by_memory_id_promote"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_ai_copilot_rate_by_message_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/rate/{messageId}"""
        return await self._call(
            OPERATIONS["post_ai_copilot_rate_by_message_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_session_by_session_id_artifact_body(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/session/{sessionId}/artifact-body"""
        return await self._call(
            OPERATIONS["post_ai_copilot_session_by_session_id_artifact_body"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_session_by_session_id_brainstorm_stop(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/session/{sessionId}/brainstorm/stop"""
        return await self._call(
            OPERATIONS["post_ai_copilot_session_by_session_id_brainstorm_stop"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_ai_copilot_session_by_session_id_workspace_env(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/session/{sessionId}/workspace/env"""
        return await self._call(
            OPERATIONS["post_ai_copilot_session_by_session_id_workspace_env"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_ai_copilot_session_by_session_id_workspace_fix(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/session/{sessionId}/workspace/fix"""
        return await self._call(
            OPERATIONS["post_ai_copilot_session_by_session_id_workspace_fix"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_session_by_session_id_workspace_heartbeat(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/session/{sessionId}/workspace/heartbeat"""
        return await self._call(
            OPERATIONS["post_ai_copilot_session_by_session_id_workspace_heartbeat"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_ai_copilot_session_by_session_id_workspace_install(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/session/{sessionId}/workspace/install"""
        return await self._call(
            OPERATIONS["post_ai_copilot_session_by_session_id_workspace_install"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_ai_copilot_session_by_session_id_workspace_prepare(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/session/{sessionId}/workspace/prepare"""
        return await self._call(
            OPERATIONS["post_ai_copilot_session_by_session_id_workspace_prepare"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_session_by_session_id_workspace_release(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/session/{sessionId}/workspace/release"""
        return await self._call(
            OPERATIONS["post_ai_copilot_session_by_session_id_workspace_release"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_ai_copilot_session_by_session_id_workspace_repairs_apply(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/session/{sessionId}/workspace/repairs/apply"""
        return await self._call(
            OPERATIONS["post_ai_copilot_session_by_session_id_workspace_repairs_apply"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_ai_copilot_session_by_session_id_workspace_restore(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/session/{sessionId}/workspace/restore"""
        return await self._call(
            OPERATIONS["post_ai_copilot_session_by_session_id_workspace_restore"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_session_by_session_id_workspace_run(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/session/{sessionId}/workspace/run"""
        return await self._call(
            OPERATIONS["post_ai_copilot_session_by_session_id_workspace_run"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_ai_copilot_session_by_session_id_workspace_stop(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/session/{sessionId}/workspace/stop"""
        return await self._call(
            OPERATIONS["post_ai_copilot_session_by_session_id_workspace_stop"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_ai_copilot_sessions(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/sessions"""
        return await self._call(
            OPERATIONS["post_ai_copilot_sessions"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_table_filters(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/table-filters"""
        return await self._call(
            OPERATIONS["post_ai_copilot_table_filters"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_table_filters_estimate(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/table-filters/estimate"""
        return await self._call(
            OPERATIONS["post_ai_copilot_table_filters_estimate"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_ai_copilot_training_consent_by_session_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /ai/copilot/training-consent/{sessionId}"""
        return await self._call(
            OPERATIONS["post_ai_copilot_training_consent_by_session_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_alert_rules_project_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /alert-rules/project/{projectId}"""
        return await self._call(
            OPERATIONS["post_alert_rules_project_by_project_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_account_setup(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/account-setup"""
        return await self._call(
            OPERATIONS["post_auth_account_setup"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_account_setup_check(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/account-setup/check"""
        return await self._call(
            OPERATIONS["post_auth_account_setup_check"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_cli_authorize(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/cli/authorize"""
        return await self._call(
            OPERATIONS["post_auth_cli_authorize"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_auth_cli_callback(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/cli/callback"""
        return await self._call(
            OPERATIONS["post_auth_cli_callback"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_cli_deny(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/cli/deny"""
        return await self._call(
            OPERATIONS["post_auth_cli_deny"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_cli_login(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/cli/login"""
        return await self._call(
            OPERATIONS["post_auth_cli_login"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_cli_requests_check(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/cli/requests/check"""
        return await self._call(
            OPERATIONS["post_auth_cli_requests_check"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_cli_token(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/cli/token"""
        return await self._call(
            OPERATIONS["post_auth_cli_token"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_forgot_password(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/forgot-password"""
        return await self._call(
            OPERATIONS["post_auth_forgot_password"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_login(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/login"""
        return await self._call(
            OPERATIONS["post_auth_login"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_logout(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/logout"""
        return await self._call(
            OPERATIONS["post_auth_logout"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_auth_logout_all(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/logout-all"""
        return await self._call(
            OPERATIONS["post_auth_logout_all"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_auth_me_linked_accounts_by_provider_start(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/me/linked-accounts/{provider}/start"""
        return await self._call(
            OPERATIONS["post_auth_me_linked_accounts_by_provider_start"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_auth_mfa_disable(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/mfa/disable"""
        return await self._call(
            OPERATIONS["post_auth_mfa_disable"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_mfa_enroll_confirm(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/mfa/enroll-confirm"""
        return await self._call(
            OPERATIONS["post_auth_mfa_enroll_confirm"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_mfa_enroll_start(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/mfa/enroll-start"""
        return await self._call(
            OPERATIONS["post_auth_mfa_enroll_start"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_auth_mfa_regenerate_codes(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/mfa/regenerate-codes"""
        return await self._call(
            OPERATIONS["post_auth_mfa_regenerate_codes"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_mfa_verify(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/mfa/verify"""
        return await self._call(
            OPERATIONS["post_auth_mfa_verify"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_reauthenticate(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/reauthenticate"""
        return await self._call(
            OPERATIONS["post_auth_reauthenticate"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_refresh(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/refresh"""
        return await self._call(
            OPERATIONS["post_auth_refresh"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_auth_reset_password(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/reset-password"""
        return await self._call(
            OPERATIONS["post_auth_reset_password"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_reset_password_check(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/reset-password/check"""
        return await self._call(
            OPERATIONS["post_auth_reset_password_check"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_session_device(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/session/device"""
        return await self._call(
            OPERATIONS["post_auth_session_device"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_session_token(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/session/token"""
        return await self._call(
            OPERATIONS["post_auth_session_token"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_auth_signup(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/signup"""
        return await self._call(
            OPERATIONS["post_auth_signup"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_sso_restart(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/sso/restart"""
        return await self._call(
            OPERATIONS["post_auth_sso_restart"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_auth_tenant_handoff(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/tenant/handoff"""
        return await self._call(
            OPERATIONS["post_auth_tenant_handoff"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_tenant_login(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/tenant/login"""
        return await self._call(
            OPERATIONS["post_auth_tenant_login"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_tenant_logout(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/tenant/logout"""
        return await self._call(
            OPERATIONS["post_auth_tenant_logout"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_auth_tenant_mfa_verify(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/tenant/mfa/verify"""
        return await self._call(
            OPERATIONS["post_auth_tenant_mfa_verify"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_tenant_refresh(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/tenant/refresh"""
        return await self._call(
            OPERATIONS["post_auth_tenant_refresh"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_auth_tenant_sso_start(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/tenant/sso/start"""
        return await self._call(
            OPERATIONS["post_auth_tenant_sso_start"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_verify_email_confirm(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/verify-email/confirm"""
        return await self._call(
            OPERATIONS["post_auth_verify_email_confirm"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_verify_email_resend(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/verify-email/resend"""
        return await self._call(
            OPERATIONS["post_auth_verify_email_resend"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_auth_verify_email_send(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /auth/verify-email/send"""
        return await self._call(
            OPERATIONS["post_auth_verify_email_send"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_checkout(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/checkout"""
        return await self._call(
            OPERATIONS["post_billing_checkout"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_enterprise_inquiry(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/enterprise/inquiry"""
        return await self._call(
            OPERATIONS["post_billing_enterprise_inquiry"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_hosting_checkout(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/hosting/checkout"""
        return await self._call(
            OPERATIONS["post_billing_hosting_checkout"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_org_by_org_id_addons(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/addons"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_addons"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_billing_org_by_org_id_addons_by_addon_id_preview(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/addons/{addonId}/preview"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_addons_by_addon_id_preview"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_org_by_org_id_addons_preview(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/addons/preview"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_addons_preview"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_org_by_org_id_cancel(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/cancel"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_cancel"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_org_by_org_id_card_check_confirm(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/card-check/confirm"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_card_check_confirm"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_org_by_org_id_card_check_session(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/card-check/session"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_card_check_session"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_org_by_org_id_change_plan(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/change-plan"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_change_plan"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_org_by_org_id_change_plan_preview(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/change-plan/preview"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_change_plan_preview"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_org_by_org_id_contacts(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/contacts"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_contacts"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_org_by_org_id_credits_purchase(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/credits/purchase"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_credits_purchase"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_org_by_org_id_pause(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/pause"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_pause"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_billing_org_by_org_id_portal(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/portal"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_portal"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_org_by_org_id_reactivate(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/reactivate"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_reactivate"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_billing_org_by_org_id_resume(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/resume"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_resume"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_billing_org_by_org_id_usage_alerts(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/org/{orgId}/usage-alerts"""
        return await self._call(
            OPERATIONS["post_billing_org_by_org_id_usage_alerts"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_promo_codes_validate(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/promo-codes/validate"""
        return await self._call(
            OPERATIONS["post_billing_promo_codes_validate"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_redeem_promo(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/redeem-promo"""
        return await self._call(
            OPERATIONS["post_billing_redeem_promo"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_billing_webhook(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /billing/webhook"""
        return await self._call(
            OPERATIONS["post_billing_webhook"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_buckets_by_bucket_id_signed_url(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /buckets/{bucketId}/signed-url"""
        return await self._call(
            OPERATIONS["post_buckets_by_bucket_id_signed_url"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_buckets_by_bucket_id_upload(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        body: bytes,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /buckets/{bucketId}/upload"""
        return await self._call(
            OPERATIONS["post_buckets_by_bucket_id_upload"],
            path=path,
            query=query,
            body=body,
            headers=headers,
        )

    async def post_buckets_by_bucket_id_upload_url(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /buckets/{bucketId}/upload-url"""
        return await self._call(
            OPERATIONS["post_buckets_by_bucket_id_upload_url"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_contact(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /contact"""
        return await self._call(
            OPERATIONS["post_contact"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_database_connector_by_project_id_query(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /database/connector/{projectId}/query"""
        return await self._call(
            OPERATIONS["post_database_connector_by_project_id_query"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_database_connector_by_project_id_test(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /database/connector/{projectId}/test"""
        return await self._call(
            OPERATIONS["post_database_connector_by_project_id_test"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_database_extensions_project_by_project_id_install(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /database/extensions/project/{projectId}/install"""
        return await self._call(
            OPERATIONS["post_database_extensions_project_by_project_id_install"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_database_wrappers_project_by_project_id_install(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /database/wrappers/project/{projectId}/install"""
        return await self._call(
            OPERATIONS["post_database_wrappers_project_by_project_id_install"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_deployments_by_deployment_id_rollback(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /deployments/{deploymentId}/rollback"""
        return await self._call(
            OPERATIONS["post_deployments_by_deployment_id_rollback"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_deployments_promote(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /deployments/promote"""
        return await self._call(
            OPERATIONS["post_deployments_promote"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_deployments_tokens(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /deployments/tokens"""
        return await self._call(
            OPERATIONS["post_deployments_tokens"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_deployments_tokens_by_token_id_revoke(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /deployments/tokens/{tokenId}/revoke"""
        return await self._call(
            OPERATIONS["post_deployments_tokens_by_token_id_revoke"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_deployments_trigger(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /deployments/trigger"""
        return await self._call(
            OPERATIONS["post_deployments_trigger"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_docs_feedback(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /docs/feedback"""
        return await self._call(
            OPERATIONS["post_docs_feedback"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_docs_search_click(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /docs/search-click"""
        return await self._call(
            OPERATIONS["post_docs_search_click"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_enterprise_inquire(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /enterprise/inquire"""
        return await self._call(
            OPERATIONS["post_enterprise_inquire"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_enterprise_quotes_by_quote_id_accept(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /enterprise/quotes/{quoteId}/accept"""
        return await self._call(
            OPERATIONS["post_enterprise_quotes_by_quote_id_accept"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_entitlements_org_by_org_id_check(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /entitlements/org/{orgId}/check"""
        return await self._call(
            OPERATIONS["post_entitlements_org_by_org_id_check"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_functions(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /functions"""
        return await self._call(
            OPERATIONS["post_functions"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_functions_by_function_id_or_name_invoke(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /functions/{functionIdOrName}/invoke"""
        return await self._call(
            OPERATIONS["post_functions_by_function_id_or_name_invoke"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_functions_by_function_id_triggers(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /functions/{functionId}/triggers"""
        return await self._call(
            OPERATIONS["post_functions_by_function_id_triggers"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_functions_secrets(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /functions/secrets"""
        return await self._call(
            OPERATIONS["post_functions_secrets"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_generated_by_table(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /generated/{table}"""
        return await self._call(
            OPERATIONS["post_generated_by_table"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_generated_by_table_bulk(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /generated/{table}/bulk"""
        return await self._call(
            OPERATIONS["post_generated_by_table_bulk"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_generated_by_table_query(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /generated/{table}/query"""
        return await self._call(
            OPERATIONS["post_generated_by_table_query"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_incidents(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /incidents"""
        return await self._call(
            OPERATIONS["post_incidents"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_incidents_bulk(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /incidents/bulk"""
        return await self._call(
            OPERATIONS["post_incidents_bulk"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_incidents_by_incident_id_ack(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /incidents/{incidentId}/ack"""
        return await self._call(
            OPERATIONS["post_incidents_by_incident_id_ack"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_incidents_by_incident_id_resolve(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /incidents/{incidentId}/resolve"""
        return await self._call(
            OPERATIONS["post_incidents_by_incident_id_resolve"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_infrastructure_poll_status(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /infrastructure/poll-status"""
        return await self._call(
            OPERATIONS["post_infrastructure_poll_status"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_integrations_deliveries_by_delivery_id_retry(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /integrations/deliveries/{deliveryId}/retry"""
        return await self._call(
            OPERATIONS["post_integrations_deliveries_by_delivery_id_retry"],
            path=path,
            query=query,
            body=body,
            headers=headers,
        )

    async def post_integrations_subscriptions(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /integrations/subscriptions"""
        return await self._call(
            OPERATIONS["post_integrations_subscriptions"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_integrations_subscriptions_by_id_test(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /integrations/subscriptions/{id}/test"""
        return await self._call(
            OPERATIONS["post_integrations_subscriptions_by_id_test"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_mcp_audit(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mcp/audit"""
        return await self._call(
            OPERATIONS["post_mcp_audit"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mcp_oauth_register(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mcp/oauth/register"""
        return await self._call(
            OPERATIONS["post_mcp_oauth_register"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mcp_oauth_requests_by_request_id_approve(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mcp/oauth/requests/{requestId}/approve"""
        return await self._call(
            OPERATIONS["post_mcp_oauth_requests_by_request_id_approve"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mcp_oauth_requests_by_request_id_deny(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mcp/oauth/requests/{requestId}/deny"""
        return await self._call(
            OPERATIONS["post_mcp_oauth_requests_by_request_id_deny"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_mcp_oauth_revoke(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mcp/oauth/revoke"""
        return await self._call(
            OPERATIONS["post_mcp_oauth_revoke"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mcp_oauth_token(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mcp/oauth/token"""
        return await self._call(
            OPERATIONS["post_mcp_oauth_token"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_me_early_welcome_seen(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /me/early/welcome-seen"""
        return await self._call(
            OPERATIONS["post_me_early_welcome_seen"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_mongodb_by_collection_aggregate(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/aggregate"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_aggregate"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_aggregate_cursor(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/aggregate/cursor"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_aggregate_cursor"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_bulk_write(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/bulkWrite"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_bulk_write"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_count(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/count"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_count"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_cursor_by_cursor_id_close(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/cursor/{cursorId}/close"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_cursor_by_cursor_id_close"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_mongodb_by_collection_cursor_by_cursor_id_next(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/cursor/{cursorId}/next"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_cursor_by_cursor_id_next"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_mongodb_by_collection_delete_many(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/deleteMany"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_delete_many"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_delete_one(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/deleteOne"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_delete_one"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_distinct(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/distinct"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_distinct"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_find(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/find"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_find"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_find_cursor(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/find/cursor"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_find_cursor"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_find_one(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/findOne"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_find_one"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_find_one_and_delete(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/findOneAndDelete"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_find_one_and_delete"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_find_one_and_replace(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/findOneAndReplace"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_find_one_and_replace"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_find_one_and_update(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/findOneAndUpdate"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_find_one_and_update"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_indexes(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/indexes"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_indexes"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_insert_many(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/insertMany"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_insert_many"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_insert_one(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/insertOne"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_insert_one"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_replace_one(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/replaceOne"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_replace_one"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_update_many(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/updateMany"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_update_many"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_by_collection_update_one(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/{collection}/updateOne"""
        return await self._call(
            OPERATIONS["post_mongodb_by_collection_update_one"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_collections(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/collections"""
        return await self._call(
            OPERATIONS["post_mongodb_collections"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_collections_by_name_rename(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/collections/{name}/rename"""
        return await self._call(
            OPERATIONS["post_mongodb_collections_by_name_rename"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_mongodb_command(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /mongodb/command"""
        return await self._call(
            OPERATIONS["post_mongodb_command"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_oauth_callback(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /oauth/callback"""
        return await self._call(
            OPERATIONS["post_oauth_callback"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_oauth_org_by_org_id_configure(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /oauth/org/{orgId}/configure"""
        return await self._call(
            OPERATIONS["post_oauth_org_by_org_id_configure"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_oauth_org_by_org_id_provider_by_provider_refresh(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /oauth/org/{orgId}/provider/{provider}/refresh"""
        return await self._call(
            OPERATIONS["post_oauth_org_by_org_id_provider_by_provider_refresh"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_onboarding_org_by_org_id_auto_setup(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /onboarding/org/{orgId}/auto-setup"""
        return await self._call(
            OPERATIONS["post_onboarding_org_by_org_id_auto_setup"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_onboarding_org_by_org_id_complete_step(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /onboarding/org/{orgId}/complete-step"""
        return await self._call(
            OPERATIONS["post_onboarding_org_by_org_id_complete_step"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_orgs(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs"""
        return await self._call(
            OPERATIONS["post_orgs"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_orgs_by_org_id_change_requests(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/{orgId}/change-requests"""
        return await self._call(
            OPERATIONS["post_orgs_by_org_id_change_requests"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_orgs_by_org_id_invites_by_invite_id_resend(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/{orgId}/invites/{inviteId}/resend"""
        return await self._call(
            OPERATIONS["post_orgs_by_org_id_invites_by_invite_id_resend"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_orgs_by_org_id_leave_requests(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/{orgId}/leave-requests"""
        return await self._call(
            OPERATIONS["post_orgs_by_org_id_leave_requests"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_orgs_by_org_id_leave_requests_by_request_id_approve(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/{orgId}/leave-requests/{requestId}/approve"""
        return await self._call(
            OPERATIONS["post_orgs_by_org_id_leave_requests_by_request_id_approve"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_orgs_by_org_id_leave_requests_by_request_id_decline(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/{orgId}/leave-requests/{requestId}/decline"""
        return await self._call(
            OPERATIONS["post_orgs_by_org_id_leave_requests_by_request_id_decline"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_orgs_by_org_id_members_invite(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/{orgId}/members/invite"""
        return await self._call(
            OPERATIONS["post_orgs_by_org_id_members_invite"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_orgs_by_org_id_support_tickets(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/{orgId}/support/tickets"""
        return await self._call(
            OPERATIONS["post_orgs_by_org_id_support_tickets"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_orgs_by_org_id_support_tickets_by_number_messages(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/{orgId}/support/tickets/{number}/messages"""
        return await self._call(
            OPERATIONS["post_orgs_by_org_id_support_tickets_by_number_messages"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_orgs_by_org_id_support_tickets_by_number_reopen(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/{orgId}/support/tickets/{number}/reopen"""
        return await self._call(
            OPERATIONS["post_orgs_by_org_id_support_tickets_by_number_reopen"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_orgs_by_org_id_support_tickets_by_number_resolve(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/{orgId}/support/tickets/{number}/resolve"""
        return await self._call(
            OPERATIONS["post_orgs_by_org_id_support_tickets_by_number_resolve"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_orgs_by_org_id_transfer(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/{orgId}/transfer"""
        return await self._call(
            OPERATIONS["post_orgs_by_org_id_transfer"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_orgs_by_org_id_transfers_by_id_resend(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/{orgId}/transfers/{id}/resend"""
        return await self._call(
            OPERATIONS["post_orgs_by_org_id_transfers_by_id_resend"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_orgs_first(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/first"""
        return await self._call(
            OPERATIONS["post_orgs_first"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_orgs_invites_accept(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/invites/accept"""
        return await self._call(
            OPERATIONS["post_orgs_invites_accept"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_orgs_invites_decline(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/invites/decline"""
        return await self._call(
            OPERATIONS["post_orgs_invites_decline"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_orgs_transfers_accept(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/transfers/accept"""
        return await self._call(
            OPERATIONS["post_orgs_transfers_accept"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_orgs_transfers_decline(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /orgs/transfers/decline"""
        return await self._call(
            OPERATIONS["post_orgs_transfers_decline"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_plans_apply(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /plans/apply"""
        return await self._call(
            OPERATIONS["post_plans_apply"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_plans_save(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /plans/save"""
        return await self._call(
            OPERATIONS["post_plans_save"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects"""
        return await self._call(
            OPERATIONS["post_projects"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_api_keys(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/api-keys"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_api_keys"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_api_keys_by_key_id_reveal(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/api-keys/{keyId}/reveal"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_api_keys_by_key_id_reveal"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_api_keys_by_key_id_revoke(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/api-keys/{keyId}/revoke"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_api_keys_by_key_id_revoke"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_api_keys_by_key_id_rotate(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/api-keys/{keyId}/rotate"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_api_keys_by_key_id_rotate"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_api_keys_split(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/api-keys/split"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_api_keys_split"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_forgot_password(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/forgot-password"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_forgot_password"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_login(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/login"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_login"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_logout(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/logout"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_logout"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_magic_send(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/magic/send"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_magic_send"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_mfa_disable(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/mfa/disable"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_mfa_disable"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_mfa_enroll_confirm(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/mfa/enroll-confirm"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_mfa_enroll_confirm"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_mfa_enroll_start(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/mfa/enroll-start"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_mfa_enroll_start"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_mfa_regenerate_codes(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/mfa/regenerate-codes"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_mfa_regenerate_codes"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_mfa_verify(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/mfa/verify"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_mfa_verify"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_oauth_by_provider_start(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/oauth/{provider}/start"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_oauth_by_provider_start"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_oauth_token(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/oauth/token"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_oauth_token"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_refresh(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/refresh"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_refresh"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_reset_password(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/reset-password"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_reset_password"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_signup(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/signup"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_signup"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_sync_users(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/sync-users"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_sync_users"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_verify_email_confirm(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/verify-email/confirm"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_verify_email_confirm"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_auth_verify_email_send(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/auth/verify-email/send"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_auth_verify_email_send"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_branches(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/branches"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_branches"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_database_dedicated(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/database/dedicated"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_database_dedicated"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_database_dedicated_restart(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/database/dedicated/restart"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_database_dedicated_restart"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_db_reset(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/db/reset"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_db_reset"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_env_vars(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/env-vars"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_env_vars"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_environments(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/environments"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_environments"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_environments_backfill_urls(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/environments/backfill-urls"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_environments_backfill_urls"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_environments_bootstrap(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/environments/bootstrap"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_environments_bootstrap"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_environments_by_env_id_domains_by_domain_id_verify(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/environments/{envId}/domains/{domainId}/verify"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_environments_by_env_id_domains_by_domain_id_verify"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_environments_by_env_id_provision_ssl(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/environments/{envId}/provision-ssl"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_environments_by_env_id_provision_ssl"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_environments_by_env_id_verify_cname(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/environments/{envId}/verify-cname"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_environments_by_env_id_verify_cname"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_environments_by_env_id_verify_domain(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/environments/{envId}/verify-domain"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_environments_by_env_id_verify_domain"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_github_branch(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/github/branch"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_github_branch"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_github_connect(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/github/connect"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_github_connect"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_github_pull(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/github/pull"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_github_pull"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_github_push(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/github/push"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_github_push"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_by_instance_id_migrate_now(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/{instanceId}/migrate-now"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_by_instance_id_migrate_now"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_by_instance_id_replica(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/{instanceId}/replica"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_by_instance_id_replica"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_by_instance_id_replica_preview(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/{instanceId}/replica-preview"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_by_instance_id_replica_preview"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_by_instance_id_resize(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/{instanceId}/resize"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_by_instance_id_resize"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_by_instance_id_resize_custom(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/{instanceId}/resize-custom"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_by_instance_id_resize_custom"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_by_instance_id_start(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/{instanceId}/start"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_by_instance_id_start"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_by_instance_id_stop(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/{instanceId}/stop"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_by_instance_id_stop"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_by_instance_id_switch(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/{instanceId}/switch"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_by_instance_id_switch"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_included_retry(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/included/retry"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_included_retry"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_migration_retry(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/migration/retry"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_migration_retry"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_migration_rollback(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/migration/rollback"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_migration_rollback"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_provision(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/provision"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_provision"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_provision_custom(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/provision-custom"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_provision_custom"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_provision_preview(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/provision-preview"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_provision_preview"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_infrastructure_restores_preview(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/infrastructure/restores/preview"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_infrastructure_restores_preview"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_members(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/members"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_members"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_promotions(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/promotions"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_promotions"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_region(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/region"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_region"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_settings_jwt_rotate(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/settings/jwt/rotate"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_settings_jwt_rotate"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_users(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/users"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_users"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_users_by_user_id_ban(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/users/{userId}/ban"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_users_by_user_id_ban"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_users_by_user_id_send_magic_link(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/users/{userId}/send-magic-link"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_users_by_user_id_send_magic_link"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_projects_by_project_id_users_by_user_id_sessions_revoke_all(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/users/{userId}/sessions/revoke-all"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_users_by_user_id_sessions_revoke_all"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_projects_by_project_id_users_by_user_id_unban(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /projects/{projectId}/users/{userId}/unban"""
        return await self._call(
            OPERATIONS["post_projects_by_project_id_users_by_user_id_unban"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_realtime_console_token(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /realtime/console-token"""
        return await self._call(
            OPERATIONS["post_realtime_console_token"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_realtime_enable_all(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /realtime/enable-all"""
        return await self._call(
            OPERATIONS["post_realtime_enable_all"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_realtime_install(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /realtime/install"""
        return await self._call(
            OPERATIONS["post_realtime_install"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_realtime_token(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /realtime/token"""
        return await self._call(
            OPERATIONS["post_realtime_token"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_realtime_uninstall(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /realtime/uninstall"""
        return await self._call(
            OPERATIONS["post_realtime_uninstall"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_regions(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /regions"""
        return await self._call(
            OPERATIONS["post_regions"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_regions_health_check(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /regions/health/check"""
        return await self._call(
            OPERATIONS["post_regions_health_check"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_rls_policies_by_policy_id_toggle(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /rls/policies/{policyId}/toggle"""
        return await self._call(
            OPERATIONS["post_rls_policies_by_policy_id_toggle"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_rls_policies_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /rls/policies/{projectId}"""
        return await self._call(
            OPERATIONS["post_rls_policies_by_project_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_schema_engine_analyze_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /schema-engine/analyze/{projectId}"""
        return await self._call(
            OPERATIONS["post_schema_engine_analyze_by_project_id"],
            path=path,
            query=query,
            body=body,
            headers=headers,
        )

    async def post_schema_engine_apply(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /schema-engine/apply"""
        return await self._call(
            OPERATIONS["post_schema_engine_apply"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_schema_engine_editor_sessions_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /schema-engine/editor-sessions/{projectId}"""
        return await self._call(
            OPERATIONS["post_schema_engine_editor_sessions_by_project_id"],
            path=path,
            query=query,
            body=None,
            headers=headers,
        )

    async def post_schema_engine_editor_sessions_by_project_id_close(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /schema-engine/editor-sessions/{projectId}/close"""
        return await self._call(
            OPERATIONS["post_schema_engine_editor_sessions_by_project_id_close"],
            path=path,
            query=query,
            body=body,
            headers=headers,
        )

    async def post_schema_engine_migrations_by_project_id_by_migration_id_rollback(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /schema-engine/migrations/{projectId}/{migrationId}/rollback"""
        return await self._call(
            OPERATIONS["post_schema_engine_migrations_by_project_id_by_migration_id_rollback"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_schema_engine_preview(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /schema-engine/preview"""
        return await self._call(
            OPERATIONS["post_schema_engine_preview"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_schema_engine_push_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /schema-engine/push/{projectId}"""
        return await self._call(
            OPERATIONS["post_schema_engine_push_by_project_id"],
            path=path,
            query=query,
            body=body,
            headers=headers,
        )

    async def post_schema_engine_query_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        query: Optional[Mapping[str, Any]] = None,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /schema-engine/query/{projectId}"""
        return await self._call(
            OPERATIONS["post_schema_engine_query_by_project_id"],
            path=path,
            query=query,
            body=body,
            headers=headers,
        )

    async def post_schema_engine_snippets_by_project_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /schema-engine/snippets/{projectId}"""
        return await self._call(
            OPERATIONS["post_schema_engine_snippets_by_project_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_schemas(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /schemas"""
        return await self._call(
            OPERATIONS["post_schemas"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_services(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /services"""
        return await self._call(
            OPERATIONS["post_services"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_services_by_service_id_deploy(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /services/{serviceId}/deploy"""
        return await self._call(
            OPERATIONS["post_services_by_service_id_deploy"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_services_by_service_id_domains(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /services/{serviceId}/domains"""
        return await self._call(
            OPERATIONS["post_services_by_service_id_domains"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_services_by_service_id_domains_by_domain_id_verify(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /services/{serviceId}/domains/{domainId}/verify"""
        return await self._call(
            OPERATIONS["post_services_by_service_id_domains_by_domain_id_verify"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_services_by_service_id_git_connect(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /services/{serviceId}/git/connect"""
        return await self._call(
            OPERATIONS["post_services_by_service_id_git_connect"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_services_by_service_id_promote(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /services/{serviceId}/promote"""
        return await self._call(
            OPERATIONS["post_services_by_service_id_promote"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_services_by_service_id_rollback(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /services/{serviceId}/rollback"""
        return await self._call(
            OPERATIONS["post_services_by_service_id_rollback"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_services_by_service_id_stop(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /services/{serviceId}/stop"""
        return await self._call(
            OPERATIONS["post_services_by_service_id_stop"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_sso_org_by_org_id_configure(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /sso/org/{orgId}/configure"""
        return await self._call(
            OPERATIONS["post_sso_org_by_org_id_configure"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_sso_org_by_org_id_connections_by_connection_id_certificates(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /sso/org/{orgId}/connections/{connectionId}/certificates"""
        return await self._call(
            OPERATIONS["post_sso_org_by_org_id_connections_by_connection_id_certificates"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_sso_org_by_org_id_connections_by_connection_id_certificates_by_cert_id_promote(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /sso/org/{orgId}/connections/{connectionId}/certificates/{certId}/promote"""
        return await self._call(
            OPERATIONS["post_sso_org_by_org_id_connections_by_connection_id_certificates_by_cert_id_promote"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_sso_org_by_org_id_connections_by_connection_id_disable(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /sso/org/{orgId}/connections/{connectionId}/disable"""
        return await self._call(
            OPERATIONS["post_sso_org_by_org_id_connections_by_connection_id_disable"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_sso_org_by_org_id_connections_by_connection_id_enable(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /sso/org/{orgId}/connections/{connectionId}/enable"""
        return await self._call(
            OPERATIONS["post_sso_org_by_org_id_connections_by_connection_id_enable"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_sso_org_by_org_id_connections_by_connection_id_metadata_import(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /sso/org/{orgId}/connections/{connectionId}/metadata/import"""
        return await self._call(
            OPERATIONS["post_sso_org_by_org_id_connections_by_connection_id_metadata_import"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_sso_org_by_org_id_connections_by_connection_id_release_account(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /sso/org/{orgId}/connections/{connectionId}/release-account"""
        return await self._call(
            OPERATIONS["post_sso_org_by_org_id_connections_by_connection_id_release_account"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_sso_org_by_org_id_connections_by_connection_id_scim_tokens(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /sso/org/{orgId}/connections/{connectionId}/scim/tokens"""
        return await self._call(
            OPERATIONS["post_sso_org_by_org_id_connections_by_connection_id_scim_tokens"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_sso_org_by_org_id_connections_by_connection_id_test(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /sso/org/{orgId}/connections/{connectionId}/test"""
        return await self._call(
            OPERATIONS["post_sso_org_by_org_id_connections_by_connection_id_test"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_sso_org_by_org_id_connections_by_connection_id_verify_domain(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /sso/org/{orgId}/connections/{connectionId}/verify-domain"""
        return await self._call(
            OPERATIONS["post_sso_org_by_org_id_connections_by_connection_id_verify_domain"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_sso_org_by_org_id_outside_members_blocked_by_user_id_restore(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /sso/org/{orgId}/outside-members/blocked/{userId}/restore"""
        return await self._call(
            OPERATIONS["post_sso_org_by_org_id_outside_members_blocked_by_user_id_restore"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_status_subscribe(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /status/subscribe"""
        return await self._call(
            OPERATIONS["post_status_subscribe"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_buckets(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/buckets"""
        return await self._call(
            OPERATIONS["post_storage_buckets"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_buckets_by_bucket_id_policies(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/buckets/{bucketId}/policies"""
        return await self._call(
            OPERATIONS["post_storage_buckets_by_bucket_id_policies"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_buckets_by_bucket_id_policies_by_policy_id_toggle(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/buckets/{bucketId}/policies/{policyId}/toggle"""
        return await self._call(
            OPERATIONS["post_storage_buckets_by_bucket_id_policies_by_policy_id_toggle"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_storage_buckets_by_bucket_id_policies_simulate(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/buckets/{bucketId}/policies/simulate"""
        return await self._call(
            OPERATIONS["post_storage_buckets_by_bucket_id_policies_simulate"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_download_url(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/download-url"""
        return await self._call(
            OPERATIONS["post_storage_download_url"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_files_copy(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/files/copy"""
        return await self._call(
            OPERATIONS["post_storage_files_copy"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_files_delete_batch(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/files/delete-batch"""
        return await self._call(
            OPERATIONS["post_storage_files_delete_batch"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_files_move(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/files/move"""
        return await self._call(
            OPERATIONS["post_storage_files_move"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_multipart_by_upload_id_abort(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/multipart/{uploadId}/abort"""
        return await self._call(
            OPERATIONS["post_storage_multipart_by_upload_id_abort"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_multipart_by_upload_id_complete(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/multipart/{uploadId}/complete"""
        return await self._call(
            OPERATIONS["post_storage_multipart_by_upload_id_complete"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_multipart_by_upload_id_part_url(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/multipart/{uploadId}/part-url"""
        return await self._call(
            OPERATIONS["post_storage_multipart_by_upload_id_part_url"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_multipart_create(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/multipart/create"""
        return await self._call(
            OPERATIONS["post_storage_multipart_create"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_multipart_resume(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/multipart/resume"""
        return await self._call(
            OPERATIONS["post_storage_multipart_resume"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_upload(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/upload"""
        return await self._call(
            OPERATIONS["post_storage_upload"],
            path=None,
            query=query,
            body=None,
            headers=headers,
        )

    async def post_storage_upload_base64(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/upload-base64"""
        return await self._call(
            OPERATIONS["post_storage_upload_base64"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_upload_from_url(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/upload-from-url"""
        return await self._call(
            OPERATIONS["post_storage_upload_from_url"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_storage_upload_url(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /storage/upload-url"""
        return await self._call(
            OPERATIONS["post_storage_upload_url"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_templates(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /templates"""
        return await self._call(
            OPERATIONS["post_templates"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_templates_create_project(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /templates/create-project"""
        return await self._call(
            OPERATIONS["post_templates_create_project"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_templates_from_project(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /templates/from-project"""
        return await self._call(
            OPERATIONS["post_templates_from_project"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_templates_from_project_preview(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /templates/from-project/preview"""
        return await self._call(
            OPERATIONS["post_templates_from_project_preview"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_templates_install_apply(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /templates/install/apply"""
        return await self._call(
            OPERATIONS["post_templates_install_apply"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_templates_install_by_install_id_rollback(
        self,
        *,
        path: Mapping[str, Any],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /templates/install/{installId}/rollback"""
        return await self._call(
            OPERATIONS["post_templates_install_by_install_id_rollback"],
            path=path,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_templates_install_preview(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /templates/install/preview"""
        return await self._call(
            OPERATIONS["post_templates_install_preview"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_users_me_change_password(
        self,
        *,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /users/me/change-password"""
        return await self._call(
            OPERATIONS["post_users_me_change_password"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_users_me_request_account_delete(
        self,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /users/me/request-account-delete"""
        return await self._call(
            OPERATIONS["post_users_me_request_account_delete"],
            path=None,
            query=None,
            body=None,
            headers=headers,
        )

    async def post_v1_data_by_project_id_by_table(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /v1/data/{projectId}/{table}"""
        return await self._call(
            OPERATIONS["post_v1_data_by_project_id_by_table"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_v1_data_by_project_id_by_table_bulk(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /v1/data/{projectId}/{table}/bulk"""
        return await self._call(
            OPERATIONS["post_v1_data_by_project_id_by_table_bulk"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_v1_data_by_project_id_by_table_query(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /v1/data/{projectId}/{table}/query"""
        return await self._call(
            OPERATIONS["post_v1_data_by_project_id_by_table_query"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def post_webhooks_github(
        self,
        *,
        query: Optional[Mapping[str, Any]] = None,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """POST /webhooks/github"""
        return await self._call(
            OPERATIONS["post_webhooks_github"],
            path=None,
            query=query,
            body=body,
            headers=headers,
        )

    async def put_ai_copilot_session_by_session_id_editor_files(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /ai/copilot/session/{sessionId}/editor-files"""
        return await self._call(
            OPERATIONS["put_ai_copilot_session_by_session_id_editor_files"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_alert_rules_by_rule_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /alert-rules/{ruleId}"""
        return await self._call(
            OPERATIONS["put_alert_rules_by_rule_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_billing_org_by_org_id_credits_auto_topup(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /billing/org/{orgId}/credits/auto-topup"""
        return await self._call(
            OPERATIONS["put_billing_org_by_org_id_credits_auto_topup"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_billing_org_by_org_id_founder_wall(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /billing/org/{orgId}/founder/wall"""
        return await self._call(
            OPERATIONS["put_billing_org_by_org_id_founder_wall"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_billing_org_by_org_id_tax_info(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /billing/org/{orgId}/tax-info"""
        return await self._call(
            OPERATIONS["put_billing_org_by_org_id_tax_info"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_buckets_by_bucket_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /buckets/{bucketId}"""
        return await self._call(
            OPERATIONS["put_buckets_by_bucket_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_functions_by_function_id_schedule(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /functions/{functionId}/schedule"""
        return await self._call(
            OPERATIONS["put_functions_by_function_id_schedule"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_functions_by_function_id_source(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /functions/{functionId}/source"""
        return await self._call(
            OPERATIONS["put_functions_by_function_id_source"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_functions_secrets_by_secret_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /functions/secrets/{secretId}"""
        return await self._call(
            OPERATIONS["put_functions_secrets_by_secret_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_me_console_look(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /me/console-look"""
        return await self._call(
            OPERATIONS["put_me_console_look"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_me_early_wall(
        self,
        *,
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /me/early/wall"""
        return await self._call(
            OPERATIONS["put_me_early_wall"],
            path=None,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_projects_by_project_id_auth_oauth_apps_by_provider(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /projects/{projectId}/auth/oauth-apps/{provider}"""
        return await self._call(
            OPERATIONS["put_projects_by_project_id_auth_oauth_apps_by_provider"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_projects_by_project_id_environments_promotion_order(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /projects/{projectId}/environments/promotion-order"""
        return await self._call(
            OPERATIONS["put_projects_by_project_id_environments_promotion_order"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_projects_by_project_id_frontend(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /projects/{projectId}/frontend"""
        return await self._call(
            OPERATIONS["put_projects_by_project_id_frontend"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_projects_by_project_id_getting_started_hidden(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /projects/{projectId}/getting-started/hidden"""
        return await self._call(
            OPERATIONS["put_projects_by_project_id_getting_started_hidden"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_projects_by_project_id_members(
        self,
        *,
        path: Mapping[str, Any],
        body: Any,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /projects/{projectId}/members"""
        return await self._call(
            OPERATIONS["put_projects_by_project_id_members"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_projects_by_project_id_members_by_user_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /projects/{projectId}/members/{userId}"""
        return await self._call(
            OPERATIONS["put_projects_by_project_id_members_by_user_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_sso_org_by_org_id_connections_by_connection_id_break_glass(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /sso/org/{orgId}/connections/{connectionId}/break-glass"""
        return await self._call(
            OPERATIONS["put_sso_org_by_org_id_connections_by_connection_id_break_glass"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_sso_org_by_org_id_connections_by_connection_id_group_mappings(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /sso/org/{orgId}/connections/{connectionId}/group-mappings"""
        return await self._call(
            OPERATIONS["put_sso_org_by_org_id_connections_by_connection_id_group_mappings"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_sso_org_by_org_id_connections_by_connection_id_require(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /sso/org/{orgId}/connections/{connectionId}/require"""
        return await self._call(
            OPERATIONS["put_sso_org_by_org_id_connections_by_connection_id_require"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_sso_org_by_org_id_outside_members_allow(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /sso/org/{orgId}/outside-members/allow"""
        return await self._call(
            OPERATIONS["put_sso_org_by_org_id_outside_members_allow"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_sso_org_by_org_id_outside_members_policy(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /sso/org/{orgId}/outside-members/policy"""
        return await self._call(
            OPERATIONS["put_sso_org_by_org_id_outside_members_policy"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_sso_org_by_org_id_security_contact(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /sso/org/{orgId}/security-contact"""
        return await self._call(
            OPERATIONS["put_sso_org_by_org_id_security_contact"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )

    async def put_storage_buckets_by_bucket_id_policies_by_policy_id(
        self,
        *,
        path: Mapping[str, Any],
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """PUT /storage/buckets/{bucketId}/policies/{policyId}"""
        return await self._call(
            OPERATIONS["put_storage_buckets_by_bucket_id_policies_by_policy_id"],
            path=path,
            query=None,
            body=body,
            headers=headers,
        )
