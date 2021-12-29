#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""This module contains a Google Bigquery sensor."""
from typing import TYPE_CHECKING, Optional, Sequence, Union

from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.sensors.base import BaseSensorOperator

if TYPE_CHECKING:
    from airflow.utils.context import Context


class BigQueryTableExistenceSensor(BaseSensorOperator):
    """
    Checks for the existence of a table in Google Bigquery.

    :param project_id: The Google cloud project in which to look for the table.
        The connection supplied to the hook must provide
        access to the specified project.
    :type project_id: str
    :param dataset_id: The name of the dataset in which to look for the table.
        storage bucket.
    :type dataset_id: str
    :param table_id: The name of the table to check the existence of.
    :type table_id: str
    :param bigquery_conn_id: The connection ID to use when connecting to
        Google BigQuery.
    :type bigquery_conn_id: str
    :param delegate_to: The account to impersonate using domain-wide delegation of authority,
        if any. For this to work, the service account making the request must have
        domain-wide delegation enabled.
    :type delegate_to: str
    :param impersonation_chain: Optional service account to impersonate using short-term
        credentials, or chained list of accounts required to get the access_token
        of the last account in the list, which will be impersonated in the request.
        If set as a string, the account must grant the originating account
        the Service Account Token Creator IAM role.
        If set as a sequence, the identities from the list must grant
        Service Account Token Creator IAM role to the directly preceding identity, with first
        account from the list granting this role to the originating account (templated).
    :type impersonation_chain: Union[str, Sequence[str]]
    """

    template_fields = (
        'project_id',
        'dataset_id',
        'table_id',
        'impersonation_chain',
    )
    ui_color = '#f0eee4'

    def __init__(
        self,
        *,
        project_id: str,
        dataset_id: str,
        table_id: str,
        bigquery_conn_id: str = 'google_cloud_default',
        delegate_to: Optional[str] = None,
        impersonation_chain: Optional[Union[str, Sequence[str]]] = None,
        **kwargs,
    ) -> None:

        super().__init__(**kwargs)
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.bigquery_conn_id = bigquery_conn_id
        self.delegate_to = delegate_to
        self.impersonation_chain = impersonation_chain

    def poke(self, context: 'Context') -> bool:
        table_uri = f'{self.project_id}:{self.dataset_id}.{self.table_id}'
        self.log.info('Sensor checks existence of table: %s', table_uri)
        hook = BigQueryHook(
            bigquery_conn_id=self.bigquery_conn_id,
            delegate_to=self.delegate_to,
            impersonation_chain=self.impersonation_chain,
        )
        return hook.table_exists(
            project_id=self.project_id, dataset_id=self.dataset_id, table_id=self.table_id
        )


class BigQueryTablePartitionExistenceSensor(BaseSensorOperator):
    """
    Checks for the existence of a partition within a table in Google Bigquery.

    :param project_id: The Google cloud project in which to look for the table.
        The connection supplied to the hook must provide
        access to the specified project.
    :type project_id: str
    :param dataset_id: The name of the dataset in which to look for the table.
        storage bucket.
    :type dataset_id: str
    :param table_id: The name of the table to check the existence of.
    :type table_id: str
    :param partition_id: The name of the partition to check the existence of.
    :type partition_id: str
    :param bigquery_conn_id: The connection ID to use when connecting to
        Google BigQuery.
    :type bigquery_conn_id: str
    :param delegate_to: The account to impersonate, if any.
        For this to work, the service account making the request must
        have domain-wide delegation enabled.
    :type delegate_to: str
    :param impersonation_chain: Optional service account to impersonate using short-term
        credentials, or chained list of accounts required to get the access_token
        of the last account in the list, which will be impersonated in the request.
        If set as a string, the account must grant the originating account
        the Service Account Token Creator IAM role.
        If set as a sequence, the identities from the list must grant
        Service Account Token Creator IAM role to the directly preceding identity, with first
        account from the list granting this role to the originating account (templated).
    :type impersonation_chain: Union[str, Sequence[str]]
    """

    template_fields = (
        'project_id',
        'dataset_id',
        'table_id',
        'partition_id',
        'impersonation_chain',
    )
    ui_color = '#f0eee4'

    def __init__(
        self,
        *,
        project_id: str,
        dataset_id: str,
        table_id: str,
        partition_id: str,
        bigquery_conn_id: str = 'google_cloud_default',
        delegate_to: Optional[str] = None,
        impersonation_chain: Optional[Union[str, Sequence[str]]] = None,
        **kwargs,
    ) -> None:

        super().__init__(**kwargs)
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.partition_id = partition_id
        self.bigquery_conn_id = bigquery_conn_id
        self.delegate_to = delegate_to
        self.impersonation_chain = impersonation_chain

    def poke(self, context: 'Context') -> bool:
        table_uri = f'{self.project_id}:{self.dataset_id}.{self.table_id}'
        self.log.info('Sensor checks existence of partition: "%s" in table: %s', self.partition_id, table_uri)
        hook = BigQueryHook(
            bigquery_conn_id=self.bigquery_conn_id,
            delegate_to=self.delegate_to,
            impersonation_chain=self.impersonation_chain,
        )
        return hook.table_partition_exists(
            project_id=self.project_id,
            dataset_id=self.dataset_id,
            table_id=self.table_id,
            partition_id=self.partition_id,
        )
