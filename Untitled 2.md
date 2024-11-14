/**

 * Licensed to the Apache Software Foundation (ASF) under one

 * or more contributor license agreements.  See the NOTICE file

 * distributed with this work for additional information

 * regarding copyright ownership.  The ASF licenses this file

 * to you under the Apache License, Version 2.0 (the

 * "License"); you may not use this file except in compliance

 * with the License.  You may obtain a copy of the License at

 *

 *   http://www.apache.org/licenses/LICENSE-2.0

 *

 * Unless required by applicable law or agreed to in writing,

 * software distributed under the License is distributed on an

 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY

 * KIND, either express or implied.  See the License for the

 * specific language governing permissions and limitations

 * under the License.

 */

import React from 'react';

import {

  ChartDataResponseResult,

  ensureIsArray,

  GenericDataType,

  getMetricLabel,

  hasGenericChartAxes,

  isAdhocColumn,

  isPhysicalColumn,

  Metric,

  QueryFormMetric,

  smartDateFormatter,

  supersetTheme,

  t,

  validateNonEmpty,

} from '@superset-ui/core';

import {

  ControlPanelConfig,

  D3_TIME_FORMAT_OPTIONS,

  sections,

  sharedControls,

  Dataset,

  getStandardizedControls,

  ColumnMeta,

  FONT_COLORS,

  FONT_WEIGHT_OPTIONS,

  ControlPanelsContainerProps,

  ControlPanelState,

  columnChoices,

  ControlSubSectionHeader,

} from '@superset-ui/chart-controls';

import Icons from '../../../../src/components/Icons';

  

import { MetricsLayoutEnum } from '../types';

  

const rightHorizontalAlign = {

  name: 'horizontalAlign',

  override: { defaultValue: 'right', width: 200 },

};

const createSortFieldConfig = (

  index: number,

  label: string,

  columnChoices: any,

) => ({

  name: `field_choice_${String.fromCharCode(97 + index)}`, // 'a', 'b', 'c'

  config: {

    type: 'SelectControl',

    // eslint-disable-next-line translation-vars/no-template-vars

    label: t(`Поле для сортировки ${label} столбца`),

    renderTrigger: true,

    mapStateToProps: (state: ControlPanelState) => ({

      choices: columnChoices(state.datasource),

    }),

    visibility: (props: ControlPanelsContainerProps) =>

      Boolean(

        props?.controls?.colOrder?.value === 'sort_by_field' &&

          props?.form_data?.groupbyColumns[index],

      ),

  },

});

// const createLabelForSort = (label: string) => (

//   <ControlSubSectionHeader>Сортировка {label} столбца</ControlSubSectionHeader>

// );

  

const createSortOrderConfig = (index: number, label: string) => ({

  name: `order_choice_${String.fromCharCode(97 + index)}`, // 'a', 'b', 'c'

  config: {

    type: 'SelectControl',

    // eslint-disable-next-line translation-vars/no-template-vars

    label: t(`Порядок сортировки ${label} столбца`),

    renderTrigger: true,

    choices: [

      [true, t('По убыванию')],

      [false, t('По возрастанию')],

    ],

    visibility: (props: ControlPanelsContainerProps) =>

      Boolean(

        props?.controls?.colOrder?.value === 'sort_by_field' &&

          props?.form_data?.groupbyColumns[index],

      ),

  },

});

const generateSortConfigs = (count: number) => {

  const configs = [];

  for (let i = 0; i < count; i += 1) {

    const label = `${i + 1}-го`;

  

    configs.push(

      // [createLabelForSort(label)],

      [

        createSortFieldConfig(i, label, columnChoices),

        createSortOrderConfig(i, label),

      ],

    );

  }

  return configs;

};

const config: ControlPanelConfig = {

  controlPanelSections: [

    { ...sections.genericTime, expanded: false },

    {

      label: t('Query'),

      expanded: true,

      controlSetRows: [

        [

          {

            name: 'groupbyColumns',

            config: {

              ...sharedControls.groupby,

              label: t('Columns'),

              description: t('Columns to group by on the columns'),

              render: ['default_collapsed_column'],

            },

          },

        ],

        [

          {

            name: 'groupbyRows',

            config: {

              ...sharedControls.groupby,

              label: t('Rows'),

              description: t('Columns to group by on the rows'),

              render: ['default_collapsed_column'],

            },

          },

        ],

        [

          {

            name: 'additionallyGroupby',

            config: {

              ...sharedControls.groupby,

              label: t('Additionally groupby'),

              render: ['default_collapsed_column'],

              visibility: (props: ControlPanelsContainerProps) =>

                Boolean(props?.controls?.colOrder?.value === 'sort_by_field'),

            },

          },

        ],

        [

          hasGenericChartAxes

            ? {

                name: 'time_grain_sqla',

                config: {

                  ...sharedControls.time_grain_sqla,

                  visibility: ({ controls }) => {

                    const dttmLookup = Object.fromEntries(

                      ensureIsArray(controls?.groupbyColumns?.options).map(

                        option => [option.column_name, option.is_dttm],

                      ),

                    );

  

                    return [

                      ...ensureIsArray(controls?.groupbyColumns.value),

                      ...ensureIsArray(controls?.groupbyRows.value),

                    ]

                      .map(selection => {

                        if (isAdhocColumn(selection)) {

                          return true;

                        }

                        if (isPhysicalColumn(selection)) {

                          return !!dttmLookup[selection];

                        }

                        return false;

                      })

                      .some(Boolean);

                  },

                },

              }

            : null,

          hasGenericChartAxes ? 'temporal_columns_lookup' : null,

        ],

        [

          {

            name: 'metrics',

            config: {

              ...sharedControls.metrics,

              validators: [validateNonEmpty],

              rerender: ['conditional_formatting'],

            },

          },

        ],

        [

          {

            name: 'metricsLayout',

            config: {

              type: 'RadioButtonControl',

              renderTrigger: true,

              label: t('Apply metrics on'),

              default: MetricsLayoutEnum.COLUMNS,

              options: [

                [MetricsLayoutEnum.COLUMNS, t('Columns')],

                [MetricsLayoutEnum.ROWS, t('Rows')],

              ],

              description: t(

                'Use metrics as a top level group for columns or for rows',

              ),

            },

          },

        ],

        ['adhoc_filters'],

        [

          {

            name: 'emit_full_hierarchy',

            config: {

              type: 'CheckboxControl',

              label: t('Cross Filter hierarchy'),

              default: false,

            },

          },

        ],

        ['series_limit'],

        [

          {

            name: 'row_limit',

            config: {

              ...sharedControls.row_limit,

              label: t('Cell limit'),

              description: t('Limits the number of cells that get retrieved.'),

            },

          },

        ],

        // TODO(kgabryje): add series_columns control after control panel is redesigned to avoid clutter

        [

          {

            name: 'series_limit_metric',

            config: {

              ...sharedControls.series_limit_metric,

              description: t(

                'Metric used to define how the top series are sorted if a series or cell limit is present. ' +

                  'If undefined reverts to the first metric (where appropriate).',

              ),

            },

          },

        ],

        [

          {

            name: 'order_desc',

            config: {

              type: 'CheckboxControl',

              label: t('Sort Descending'),

              default: true,

              description: t('Whether to sort descending or ascending'),

            },

          },

        ],

      ],

    },

    {

      label: t('Options'),

      expanded: true,

      tabOverride: 'data',

      controlSetRows: [

        [

          {

            name: 'default_collapsed_row',

            config: {

              type: 'SelectControl',

              label: t('Default collapsed row'),

              renderTrigger: true,

              rerender: [],

              multi: false,

              visibility: explore =>

                !!explore?.controls?.rowSubTotals?.value &&

                !!ensureIsArray(explore?.controls?.groupbyRows?.value).length,

              shouldMapStateToProps() {

                return true;

              },

              mapStateToProps(state) {

                const columns = state?.datasource?.columns as ColumnMeta[];

                const columns_map = columns.reduce(

                  (acc, { column_name, verbose_name }) => {

                    acc[column_name] = verbose_name ?? column_name;

                    return acc;

                  },

                  {},

                );

                const groupbyRows = ensureIsArray(

                  state?.form_data?.groupbyRows,

                );

                const options = groupbyRows.map((label, i) => ({

                  label: columns_map[label] ?? label.label ?? label,

                  value: groupbyRows.length - i - 1,

                }));

                return { options };

              },

            },

          },

        ],

        [

          {

            name: 'default_collapsed_col',

            config: {

              type: 'SelectControl',

              label: t('Default collapsed column'),

              renderTrigger: true,

              rerender: [],

              multi: false,

              visibility: explore =>

                !!explore?.controls?.colSubTotals?.value &&

                !!ensureIsArray(explore?.controls?.groupbyColumns?.value)

                  .length,

              shouldMapStateToProps() {

                return true;

              },

              mapStateToProps(state) {

                const columns = state?.datasource?.columns as ColumnMeta[];

                const columns_map = columns.reduce(

                  (acc, { column_name, verbose_name }) => {

                    acc[column_name] = verbose_name;

                    return acc;

                  },

                  {},

                );

                const groupbyColumns = ensureIsArray(

                  state?.form_data?.groupbyColumns,

                );

                const options = groupbyColumns.map((label, i) => ({

                  label: columns_map[label] ?? label,

                  value: groupbyColumns.length - i - 1,

                }));

                return { options };

              },

            },

          },

        ],

        [

          {

            name: 'default_collapsed_metrics',

            config: {

              type: 'SelectControl',

              label: t('Default collapsed metric'),

              renderTrigger: true,

              default: undefined,

              rerender: [],

              multi: true,

              visibility: explore =>

                !!explore?.controls?.colSubTotals?.value &&

                !!ensureIsArray(explore?.controls?.metrics?.value).length,

              shouldMapStateToProps() {

                return true;

              },

              mapStateToProps(state) {

                const datasource_metrics = (state?.datasource as Dataset)

                  ?.metrics as Metric[];

                const metrics_map = datasource_metrics.reduce(

                  (acc, { metric_name, verbose_name }) => {

                    acc[metric_name] = verbose_name;

                    return acc;

                  },

                  {},

                );

                const metrics = ensureIsArray(state?.form_data?.metrics);

                const options = metrics.map(metric => {

                  const label = getMetricLabel(metric);

                  return {

                    label: metrics_map[label] ?? label,

                    value: label,

                  };

                });

                return { options };

              },

            },

          },

        ],

        [

          {

            name: 'aggregateFunction',

            config: {

              type: 'SelectControl',

              label: t('Aggregation function'),

              clearable: false,

              choices: [

                ['Count', t('Count')],

                ['Count Unique Values', t('Count Unique Values')],

                ['List Unique Values', t('List Unique Values')],

                ['Sum', t('Sum')],

                ['Average', t('Average')],

                ['Median', t('Median')],

                ['Sample Variance', t('Sample Variance')],

                ['Sample Standard Deviation', t('Sample Standard Deviation')],

                ['Minimum', t('Minimum')],

                ['Maximum', t('Maximum')],

                ['First', t('First')],

                ['Last', t('Last')],

                ['Sum as Fraction of Total', t('Sum as Fraction of Total')],

                ['Sum as Fraction of Rows', t('Sum as Fraction of Rows')],

                ['Sum as Fraction of Columns', t('Sum as Fraction of Columns')],

                ['Count as Fraction of Total', t('Count as Fraction of Total')],

                ['Count as Fraction of Rows', t('Count as Fraction of Rows')],

                [

                  'Count as Fraction of Columns',

                  t('Count as Fraction of Columns'),

                ],

              ],

              default: 'Sum',

              description: t(

                'Aggregate function to apply when pivoting and computing the total rows and columns',

              ),

              renderTrigger: true,

            },

          },

        ],

        [

          {

            name: 'totalsByMetric',

            config: {

              type: 'CheckboxControl',

              label: t('Use metric aggration for total'),

              default: false,

              renderTrigger: false,

              description: t('Use metric aggration for total'),

            },

          },

        ],

        [

          {

            name: 'rowTotals',

            config: {

              type: 'CheckboxControl',

              label: t('Show rows total'),

              default: false,

              renderTrigger: true,

              description: t('Display row level total'),

            },

          },

        ],

        [

          {

            name: 'rowSubTotals',

            config: {

              type: 'CheckboxControl',

              label: t('Show rows subtotal'),

              default: false,

              renderTrigger: true,

              description: t('Display row level subtotal'),

            },

          },

        ],

        [

          {

            name: 'colTotals',

            config: {

              type: 'CheckboxControl',

              label: t('Show columns total'),

              default: false,

              renderTrigger: true,

              description: t('Display column level total'),

            },

          },

        ],

        [

          {

            name: 'colSubTotals',

            config: {

              type: 'CheckboxControl',

              label: t('Show columns subtotal'),

              default: false,

              renderTrigger: true,

              description: t('Display column level subtotal'),

            },

          },

        ],

        [

          {

            name: 'hideExpandedCols',

            config: {

              type: 'CheckboxControl',

              label: t('Hide expanded cols'),

              default: false,

              renderTrigger: true,

            },

          },

        ],

        [

          {

            name: 'hideExpandedRows',

            config: {

              type: 'CheckboxControl',

              label: t('Hide expanded rows'),

              default: false,

              renderTrigger: true,

            },

          },

        ],

        [

          {

            name: 'transposePivot',

            config: {

              type: 'CheckboxControl',

              label: t('Transpose pivot'),

              default: false,

              description: t('Swap rows and columns'),

              renderTrigger: true,

            },

          },

        ],

        [

          {

            name: 'combineMetric',

            config: {

              type: 'CheckboxControl',

              label: t('Combine metrics'),

              default: false,

              description: t(

                'Display metrics side by side within each column, as ' +

                  'opposed to each column being displayed side by side for each metric.',

              ),

              renderTrigger: true,

            },

          },

        ],

        [

          {

            name: 'conditionalFormatTotals',

            config: {

              type: 'CheckboxControl',

              label: t('Format totals with conditions'),

              default: false,

              renderTrigger: true,

            },

          },

        ],

      ],

    },

    {

      label: t('Options'),

      expanded: true,

      controlSetRows: [

        [

          {

            name: 'valueFormat',

            config: {

              ...sharedControls.y_axis_format,

              label: t('Value format'),

            },

          },

        ],

        ['currency_format'],

        [

          {

            name: 'date_format',

            config: {

              type: 'SelectControl',

              freeForm: true,

              label: t('Date format'),

              default: smartDateFormatter.id,

              renderTrigger: true,

              choices: D3_TIME_FORMAT_OPTIONS,

              description: t('D3 time format for datetime columns'),

            },

          },

        ],

        [

          {

            name: 'rowOrder',

            config: {

              type: 'SelectControl',

              label: t('Sort rows by'),

              default: 'key_a_to_z',

              choices: [

                // [value, label]

                ['key_a_to_z', t('key a-z')],

                ['key_z_to_a', t('key z-a')],

                ['value_a_to_z', t('value ascending')],

                ['value_z_to_a', t('value descending')],

                ['', 'Не сортировать'],

              ],

              renderTrigger: true,

              description: (

                <>

                  <div>{t('Change order of rows.')}</div>

                  <div>{t('Available sorting modes:')}</div>

                  <ul>

                    <li>{t('By key: use row names as sorting key')}</li>

                    <li>{t('By value: use metric values as sorting key')}</li>

                  </ul>

                </>

              ),

            },

          },

        ],

        [

          {

            name: 'colOrder',

            config: {

              type: 'SelectControl',

              label: t('Sort columns by'),

              default: 'key_a_to_z',

              choices: [

                // [value, label]

                ['key_a_to_z', t('key a-z')],

                ['key_z_to_a', t('key z-a')],

                ['value_a_to_z', t('value ascending')],

                ['value_z_to_a', t('value descending')],

                ['custom_order', t('Произвольный порядок')],

                ['sort_by_field', t('Сортировка по полю')],

                ['', 'Не сортировать'],

              ],

              renderTrigger: true,

              description: (

                <>

                  <div>{t('Change order of columns.')}</div>

                  <div>{t('Available sorting modes:')}</div>

                  <ul>

                    <li>{t('By key: use column names as sorting key')}</li>

                    <li>{t('By value: use metric values as sorting key')}</li>

                  </ul>

                </>

              ),

            },

          },

        ],

        [

          {

            name: 'custom_col_order',

            config: {

              type: 'TextControl',

              label: t('Порядок столбцов'),

              renderTrigger: true,

              default: '',

              debounceDelay: 1000,

              visibility: ({ controls }: ControlPanelsContainerProps) =>

                controls?.colOrder?.value === 'custom_order',

            },

          },

        ],

        ...generateSortConfigs(5),

        // [

        //   {

        //     name: 'field_choice_a',

        //     config: {

        //       type: 'SelectControl',

        //       label: t('Поле для сортироки первого столбца'),

        //       renderTrigger: true,

        //       mapStateToProps: (state: ControlPanelState) => ({

        //         choices: columnChoices(state.datasource),

        //       }),

        //       visibility: (props: ControlPanelsContainerProps) =>

        //         Boolean(

        //           props?.controls?.colOrder?.value === 'sort_by_field' &&

        //             props?.form_data?.groupbyColumns[0],

        //         ),

        //     },

        //   },

        //   {

        //     name: 'order_choice_a',

        //     config: {

        //       type: 'SelectControl',

        //       label: t('Порядок сортироки первого столбца'),

        //       renderTrigger: true,

        //       choices: [

        //         // [value, label]

        //         [true, t('По убыванию')],

        //         [false, t('По возрастанию')],

        //       ],

        //       visibility: (props: ControlPanelsContainerProps) =>

        //         Boolean(

        //           props?.controls?.colOrder?.value === 'sort_by_field' &&

        //             props?.form_data?.groupbyColumns[0],

        //         ),

        //     },

        //   },

        // ],

        // [

        //   {

        //     name: 'field_choice_b',

        //     config: {

        //       type: 'SelectControl',

        //       label: t('Поле для сортировки второго столбца'),

        //       renderTrigger: true,

        //       mapStateToProps: (state: ControlPanelState) => ({

        //         choices: columnChoices(state.datasource),

        //       }),

        //       visibility: (props: ControlPanelsContainerProps) =>

        //         Boolean(

        //           props?.controls?.colOrder?.value === 'sort_by_field' &&

        //             props?.form_data?.groupbyColumns[1],

        //         ),

        //     },

        //   },

        //   {

        //     name: 'order_choice_b',

        //     config: {

        //       type: 'SelectControl',

        //       label: t('Порядок сортироки второго столбца'),

        //       renderTrigger: true,

        //       choices: [

        //         // [value, label]

        //         [true, t('По убыванию')],

        //         [false, t('По возрастанию')],

        //       ],

        //       visibility: (props: ControlPanelsContainerProps) =>

        //         Boolean(

        //           props?.controls?.colOrder?.value === 'sort_by_field' &&

        //             props?.form_data?.groupbyColumns[1],

        //         ),

        //     },

        //   },

        // ],

        // [

        //   {

        //     name: 'field_choice_c',

        //     config: {

        //       type: 'SelectControl',

        //       label: t('Поле для сортировки третьего столбца'),

        //       renderTrigger: true,

        //       mapStateToProps: (state: ControlPanelState) => {

        //         console.log(

        //           'columnChoices(state.datasource): ',

        //           columnChoices(state.datasource),

        //         );

        //         return {

        //           choices: columnChoices(state.datasource),

        //         };

        //       },

        //       visibility: (props: ControlPanelsContainerProps) =>

        //         Boolean(

        //           props?.controls?.colOrder?.value === 'sort_by_field' &&

        //             props?.form_data?.groupbyColumns[2],

        //         ),

        //     },

        //   },

        //   {

        //     name: 'order_choice_c',

        //     config: {

        //       type: 'SelectControl',

        //       label: t('Порядок сортироки третьего столбца'),

        //       renderTrigger: true,

        //       choices: [

        //         // [value, label]

        //         [true, t('По убыванию')],

        //         [false, t('По возрастанию')],

        //       ],

        //       visibility: (props: ControlPanelsContainerProps) =>

        //         Boolean(

        //           props?.controls?.colOrder?.value === 'sort_by_field' &&

        //             props?.form_data?.groupbyColumns[2],

        //         ),

        //     },

        //   },

        // ],

        // [

        //   {

        //     name: 'column_config_sort',

        //     config: {

        //       type: 'ColumnConfigControl',

        //       description: t('Further customize how to display each column'),

        //       renderTrigger: true,

        //       configFormLayout: {

        //         [GenericDataType.STRING]: [

        //           ['columnFieldSelect'], // , rightHorizontalAlign

        //         ],

        //       },

        //       shouldMapStateToProps() {

        //         return true;

        //       },

        //       mapStateToProps(state, _, chart) {

        //         const queryResponse = chart?.queriesResponse?.[0] as

        //           | ChartDataResponseResult

        //           | undefined;

        //         const formData = state?.form_data;

        //         console.log('chart: ', chart);

        //         console.log('formData: ', formData);

        //         console.log('explore: ', state);

        //         console.log('explore: ', state);

        //         return {

        //           queryResponse: {

        //             ...queryResponse,

        //             colnames: [

        //               ...formData?.groupbyColumns,

        //               // ...[formData?.metrics?.map(el => el?.label)],

        //             ],

        //           },

        //           state,

        //         };

        //       },

        //       visibility: ({ controls }: ControlPanelsContainerProps) =>

        //         controls?.colOrder?.value === 'sort_by_field',

        //     },

        //   },

        // ],

        [

          {

            name: 'rowSubtotalPosition',

            config: {

              type: 'SelectControl',

              label: t('Rows subtotal position'),

              default: false,

              choices: [

                // [value, label]

                [true, t('Top')],

                [false, t('Bottom')],

              ],

              renderTrigger: true,

              description: t('Position of row level subtotal'),

            },

          },

        ],

        [

          {

            name: 'colSubtotalPosition',

            config: {

              type: 'SelectControl',

              label: t('Columns subtotal position'),

              default: false,

              choices: [

                // [value, label]

                [true, t('Left')],

                [false, t('Right')],

              ],

              renderTrigger: true,

              description: t('Position of column level subtotal'),

            },

          },

        ],

        [

          {

            name: 'column_config',

            config: {

              type: 'ColumnConfigControl',

              description: t('Further customize how to display each column'),

              renderTrigger: true,

              configFormLayout: {

                [GenericDataType.NUMERIC]: [

                  ['columnWidth', rightHorizontalAlign], // , rightHorizontalAlign

                  ['truncateLongCells', 'columnFontWeight'],

                  ['showTotal'],

                  ['showSubTotal'],

                  ['d3NumberFormat'],

                ],

                [GenericDataType.TEMPORAL]: [

                  ['columnWidth', rightHorizontalAlign], // , rightHorizontalAlign

                  ['truncateLongCells', 'columnFontWeight'],

                  ['showTotal'],

                  ['showSubTotal'],

                ],

                [GenericDataType.STRING]: [

                  ['columnWidth', rightHorizontalAlign], // , rightHorizontalAlign

                  ['truncateLongCells', 'columnFontWeight'],

                  ['showTotal'],

                  ['showSubTotal'],

                ],

                [GenericDataType.BOOLEAN]: [

                  ['columnWidth', rightHorizontalAlign], // , rightHorizontalAlign

                  ['truncateLongCells', 'columnFontWeight'],

                  ['showTotal'],

                  ['showSubTotal'],

                ],

              },

              shouldMapStateToProps() {

                return true;

              },

              mapStateToProps(explore, _, chart) {

                const queryResponse = chart?.queriesResponse?.[0] as

                  | ChartDataResponseResult

                  | undefined;

                return {

                  queryResponse,

                  emitFilter: explore?.controls?.table_filter?.value,

                };

              },

            },

          },

        ],

  

        [

          {

            name: 'conditional_formatting',

            config: {

              type: 'ConditionalFormattingControl',

              renderTrigger: true,

              label: t('Conditional formatting'),

              description: t('Apply conditional color formatting to metrics'),

              shouldMapStateToProps() {

                return true;

              },

              mapStateToProps(explore, _, chart) {

                const values =

                  (explore?.controls?.metrics?.value as QueryFormMetric[]) ??

                  [];

                const verboseMap = explore?.datasource?.hasOwnProperty(

                  'verbose_map',

                )

                  ? (explore?.datasource as Dataset)?.verbose_map

                  : explore?.datasource?.columns ?? {};

                const chartStatus = chart?.chartStatus;

                const { colnames, coltypes } =

                  chart?.queriesResponse?.[0] ?? {};

                const metricColumn = values.map(value => {

                  if (typeof value === 'string') {

                    return {

                      value,

                      label: verboseMap[value] ?? value,

                      dataType:

                        colnames &&

                        coltypes[colnames?.indexOf(verboseMap[value] ?? value)],

                    };

                  }

                  return {

                    value: value.label,

                    label: value.label,

                    dataType:

                      colnames && coltypes[colnames?.indexOf(value.label)],

                  };

                });

                return {

                  removeIrrelevantConditions: chartStatus === 'success',

                  columnOptions: metricColumn,

                  verboseMap,

                };

              },

            },

          },

        ],

      ],

    },

    {

      label: t('Заголовок'),

      expanded: false,

      controlSetRows: [

        // Label

        [

          // {

          //   name: 'fontSize',

          //   config: {

          //     type: 'TextControl',

          //     label: 'Размер шрифта',

          //     placeholder: t('auto'),

          //     description: 'Ввод размера шрифта для всей таблицы',

          //     renderTrigger: true,

          //   },

          // },

          {

            name: 'header_font_size',

            config: {

              type: 'SliderControl',

              label: 'Размер шрифта',

              renderTrigger: true,

              min: 4,

              max: 40,

              step: 1,

              default: 12,

              description: 'Размер шрифта',

            },

          },

          {

            name: 'header_label_color',

            config: {

              type: 'SelectControl',

              label: 'Цвет текста',

              description: 'Цвет текста в заголовке таблице',

              freeForm: true,

              clearable: false,

              renderTrigger: true,

              choices: FONT_COLORS,

            },

          },

        ],

        [

          {

            name: 'header_align',

            config: {

              type: 'RadioButtonControl',

              label: 'Выравнивание',

              description: 'Горизонтальное выравнивание заголовка',

              default: 'left',

              renderTrigger: true,

              options: [

                ['left', <Icons.AlignLeftOutlined iconSize="m" />],

                ['center', <Icons.AlignCenterOutlined iconSize="m" />],

                ['right', <Icons.AlignRightOutlined iconSize="m" />],

              ],

            },

          },

          {

            name: 'header_background_color',

            config: {

              type: 'SelectControl',

              label: 'Цвет фона',

              description: 'Цвет фона в заголовке таблицы',

              freeForm: true,

              clearable: false,

              renderTrigger: true,

              choices: [

                ['', t('По умолчанию')],

                [supersetTheme.colors.ENorange, t('EN+ Оранжевый')],

                [supersetTheme.colors.white, t('Белый')],

              ],

            },

          },

        ],

        [

          {

            name: 'header_border_color',

            config: {

              type: 'SelectControl',

              label: 'Цвет границ',

              description: 'Цвет границ во всей таблицы',

              freeForm: true,

              clearable: false,

              renderTrigger: true,

              choices: [

                ['', t('По умолчанию')],

                [supersetTheme.colors.grayscale.dark2, t('Черный')],

                [supersetTheme.colors.grayscale.base, t('Темно серый')],

                [supersetTheme.colors.ENorange, t('EN+ Оранжевый')],

                [supersetTheme.colors.white, t('Белый')],

              ],

            },

          },

          {

            name: 'min_width',

            config: {

              type: 'TextControl',

              label: 'Минимальная ширина',

              placeholder: 'auto',

              description: 'Ввод минимальной ширины',

              renderTrigger: true,

            },

          },

        ],

        [

          {

            name: 'header_font_weight',

            config: {

              type: 'SelectControl',

              label: 'Жирность',

              description: 'Жирность текста',

              freeForm: true,

              clearable: true,

              renderTrigger: true,

              choices: FONT_WEIGHT_OPTIONS,

            },

          },

        ],

      ],

    },

    {

      label: t('Строки'),

      expanded: false,

      controlSetRows: [

        [

          {

            name: 'body_font_size',

            config: {

              type: 'SliderControl',

              label: 'Размер шрифта',

              renderTrigger: true,

              min: 4,

              max: 40,

              step: 1,

              default: 12,

              description: 'Размер шрифта',

            },

          },

          {

            name: 'body_label_color',

            config: {

              type: 'SelectControl',

              label: 'Цвет текста',

              description: 'Цвет текста в заголовке таблице',

              freeForm: true,

              clearable: false,

              renderTrigger: true,

              choices: FONT_COLORS,

            },

          },

        ],

        [

          {

            name: 'body_align',

            config: {

              type: 'RadioButtonControl',

              label: 'Выравнивание значений',

              description: 'Горизонтальное выравнивание значений',

              default: 'left',

              renderTrigger: true,

              options: [

                ['left', <Icons.AlignLeftOutlined iconSize="m" />],

                ['center', <Icons.AlignCenterOutlined iconSize="m" />],

                ['right', <Icons.AlignRightOutlined iconSize="m" />],

                ['', <Icons.CloseOutlined iconSize="m" title="Отменить" />],

              ],

            },

          },

          {

            name: 'body_background_color',

            config: {

              type: 'SelectControl',

              label: 'Цвет фона',

              description: 'Цвет фона в заголовке таблицы',

              freeForm: true,

              clearable: false,

              renderTrigger: true,

              choices: [

                ['', t('По умолчанию')],

                [supersetTheme.colors.ENorange, t('EN+ Оранжевый')],

                [supersetTheme.colors.white, t('Белый')],

              ],

            },

          },

        ],

        [

          {

            name: 'body_row_align',

            config: {

              type: 'RadioButtonControl',

              label: 'Выравнивание строк',

              description: 'Горизонтальное выравнивание строк',

              default: 'left',

              renderTrigger: true,

              options: [

                ['left', <Icons.AlignLeftOutlined iconSize="m" />],

                ['center', <Icons.AlignCenterOutlined iconSize="m" />],

                ['right', <Icons.AlignRightOutlined iconSize="m" />],

                ['', <Icons.CloseOutlined iconSize="m" title="Отменить" />],

              ],

            },

          },

          {

            name: 'body_border_color',

            config: {

              type: 'SelectControl',

              label: 'Цвет границ',

              description: 'Цвет границ во всей таблицы',

              freeForm: true,

              clearable: false,

              renderTrigger: true,

              choices: [

                ['', t('По умолчанию')],

                [supersetTheme.colors.grayscale.dark2, t('Черный')],

                [supersetTheme.colors.grayscale.base, t('Темно серый')],

                [supersetTheme.colors.ENorange, t('EN+ Оранжевый')],

                [supersetTheme.colors.white, t('Белый')],

              ],

            },

          },

        ],

        [

          {

            name: 'body_font_weight',

            config: {

              type: 'SelectControl',

              label: 'Жирность',

              description: 'Жирность текста',

              freeForm: true,

              clearable: true,

              renderTrigger: true,

              choices: FONT_WEIGHT_OPTIONS,

            },

          },

        ],

      ],

    },

  ],

  formDataOverrides: formData => {

    const groupbyColumns = getStandardizedControls().controls.columns.filter(

      col => !ensureIsArray(formData.groupbyRows).includes(col),

    );

    getStandardizedControls().controls.columns =

      getStandardizedControls().controls.columns.filter(

        col => !groupbyColumns.includes(col),

      );

    return {

      ...formData,

      metrics: getStandardizedControls().popAllMetrics(),

      groupbyColumns,

    };

  },

};

  

export default config;