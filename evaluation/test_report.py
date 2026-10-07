"""Local data/format tests. No model calls or submitted-code execution."""
import copy
import unittest

import report


class ReportTests(unittest.TestCase):
    def setUp(self):
        (self.summary, self.attempts, self.schedule, self.definitions,
         self.initial, self.initial_attempts, self.initial_schedule) = report.load_inputs()
        self.rendered = report.tables(self.summary, self.attempts, self.initial)
        self.docs = {name: path.read_text(encoding='utf-8') for name, path in report.DOC_PATHS.items()}

    def validate(self):
        report.validate(self.summary, self.attempts, self.schedule, self.definitions)

    def validate_initial(self):
        report.validate_initial(self.initial, self.initial_attempts, self.initial_schedule)

    def test_saved_inputs_and_current_docs(self):
        self.validate()
        self.validate_initial()
        report.check_docs(self.rendered, self.docs)
        report.check_claims(self.summary, self.attempts, self.initial, self.docs)

    def test_rejects_missing_attempt(self):
        self.attempts.pop()
        with self.assertRaisesRegex(ValueError, 'missing, extra, or duplicate attempt'):
            self.validate()

    def test_rejects_duplicate_attempt(self):
        self.attempts[-1] = copy.deepcopy(self.attempts[0])
        with self.assertRaisesRegex(ValueError, 'missing, extra, or duplicate attempt'):
            self.validate()

    def test_rejects_swapped_condition(self):
        self.attempts[0]['condition'] = 'C'
        with self.assertRaisesRegex(ValueError, 'condition or schedule mismatch'):
            self.validate()

    def test_rejects_stale_summary_count(self):
        self.summary['conditions']['S']['counts']['pass'] -= 1
        with self.assertRaisesRegex(ValueError, 'stale condition counts'):
            self.validate()

    def test_rejects_missing_requirement(self):
        self.attempts[0]['requirements'].pop()
        with self.assertRaises(ValueError):
            self.validate()

    def test_rejects_unknown_status(self):
        self.attempts[0]['requirements'][0]['status'] = 'pending'
        with self.assertRaisesRegex(ValueError, 'unknown requirement status'):
            self.validate()

    def test_rejects_stale_table(self):
        self.docs['overview'] = self.docs['overview'].replace('159/159', '158/159')
        with self.assertRaisesRegex(ValueError, 'stale or missing result table'):
            report.check_docs(self.rendered, self.docs)

    def test_rejects_swapped_table_labels(self):
        self.docs['overview'] = self.docs['overview'].replace('| With skill | Baseline |', '| Baseline | With skill |')
        with self.assertRaisesRegex(ValueError, 'stale or missing result table'):
            report.check_docs(self.rendered, self.docs)

    def test_rejects_absent_caveats_in_either_report(self):
        for name, guards in report.GUARDS.items():
            for text in guards:
                with self.subTest(document=name, caveat=text):
                    docs = self.docs.copy()
                    docs[name] = docs[name].replace(text, '')
                    with self.assertRaisesRegex(ValueError, 'missing condition definition or limitation'):
                        report.check_docs(self.rendered, docs)

    def test_preserves_zero_delta(self):
        for table in (self.rendered['overview'], self.rendered['study']):
            self.assertIn('| 159/159 | 159/159 | 0 |', table)

    def test_rejects_missing_duplicate_extra_and_reordered_table_rows(self):
        for document, names in report.DOC_TABLES.items():
            for name in names:
                table = self.rendered[name]
                lines = table.splitlines()
                mutations = {
                    'missing': lines[:-1],
                    'duplicate': [*lines, lines[-1]],
                    'extra': [*lines, '| Pooled total | 199/199 | 199/199 |'],
                    'reordered': [*lines[:2], *reversed(lines[2:])],
                }
                for mutation, changed in mutations.items():
                    with self.subTest(table=name, mutation=mutation):
                        docs = self.docs.copy()
                        docs[document] = docs[document].replace(table, '\n'.join(changed))
                        with self.assertRaisesRegex(ValueError, 'result table'):
                            report.check_docs(self.rendered, docs)

    def test_rejects_duplicate_or_extra_table(self):
        for document, names in report.DOC_TABLES.items():
            for extra in (self.rendered[names[0]], '| Combined | Score |\n|---|---|\n| Pooled | 199/199 |'):
                with self.subTest(document=document, extra=extra):
                    docs = self.docs.copy()
                    docs[document] += '\n\n' + extra + '\n'
                    with self.assertRaisesRegex(ValueError, 'result table'):
                        report.check_docs(self.rendered, docs)

    def test_rejects_result_table_hidden_in_code_fence(self):
        for fence in ('```', '~~~', '````'):
            with self.subTest(fence=fence):
                docs = self.docs.copy()
                table = self.rendered['index']
                docs['index'] = docs['index'].replace(table, f'{fence}markdown\n{table}\n{fence}')
                with self.assertRaisesRegex(ValueError, 'result table'):
                    report.check_docs(self.rendered, docs)

    def test_rejects_body_rows_without_outer_pipes(self):
        for document, names in report.DOC_TABLES.items():
            for name in names:
                table = self.rendered[name]
                row = table.splitlines()[-1]
                for extra in (row.strip('|'), row.lstrip('|'), row.rstrip('|'), 'Pooled total'):
                    with self.subTest(table=name, extra=extra):
                        docs = self.docs.copy()
                        docs[document] = docs[document].replace(table, table + '\n' + extra)
                        with self.assertRaisesRegex(ValueError, 'result table'):
                            report.check_docs(self.rendered, docs)

    def test_rejects_extra_tables_without_outer_pipes(self):
        for header, separator in (('Study | With skill | Baseline', '--- | --- | ---'),
                                  ('| Study | With skill | Baseline', '| --- | --- | ---'),
                                  ('Study | With skill | Baseline |', '--- | --- | --- |'),
                                  ('> Study | With skill | Baseline', '> --- | --- | ---')):
            with self.subTest(header=header):
                docs = self.docs.copy()
                docs['index'] += f'\n\n{header}\n{separator}\nPooled total | 199/199 | 199/199\n'
                with self.assertRaisesRegex(ValueError, 'result table'):
                    report.check_docs(self.rendered, docs)

    def test_block_like_body_text_cannot_hide_extra_rows(self):
        for prefix in ('1234567890. ', '- ', '* ', '> ', '### '):
            with self.subTest(prefix=prefix):
                docs = self.docs.copy()
                table = self.rendered['index']
                docs['index'] = docs['index'].replace(table, table + '\n' + prefix +
                                                     'Pooled total | 199/199 | 199/199 | 0 |')
                with self.assertRaisesRegex(ValueError, 'result table'):
                    report.check_docs(self.rendered, docs)

    def test_rejects_expected_table_hidden_in_html_comment(self):
        for document, names in report.DOC_TABLES.items():
            for name in names:
                for opening, closing in (('<!--\n', '\n-->'), ('<!--', '-->'), ('<!--\n', '')):
                    with self.subTest(table=name, opening=opening, closing=closing):
                        docs = self.docs.copy()
                        table = self.rendered[name]
                        docs[document] = docs[document].replace(table, opening + table + closing)
                        with self.assertRaisesRegex(ValueError, 'result table|raw HTML'):
                            report.check_docs(self.rendered, docs)

    def test_hidden_caveats_and_numeric_statements_are_not_evidence(self):
        for wrapper in ('<!-- {} -->', '\n```\n{}\n```\n'):
            with self.subTest(wrapper=wrapper):
                docs = self.docs.copy()
                guard = 'Do not pool their denominators.'
                docs['index'] = docs['index'].replace(guard, wrapper.format(guard))
                with self.assertRaisesRegex(ValueError, 'condition definition or limitation|raw HTML'):
                    report.check_docs(self.rendered, docs)
                docs = self.docs.copy()
                statement = 'All 24 rows are retained in dispatch order.'
                docs['attempts'] = docs['attempts'].replace(statement, wrapper.format(statement))
                with self.assertRaisesRegex(ValueError, 'numeric statement|raw HTML'):
                    report.check_claims(self.summary, self.attempts, self.initial, docs)

    def test_invalid_fences_do_not_hide_extra_tables(self):
        for opener in ('```bad`info', '    ```'):
            with self.subTest(opener=opener):
                docs = self.docs.copy()
                docs['index'] += f'\n\n{opener}\n\nPooled | Total\n--- | ---\nAll | 199/199\n'
                with self.assertRaisesRegex(ValueError, 'result table'):
                    report.check_docs(self.rendered, docs)

    def test_comments_cannot_synthesize_fences_or_table_headers(self):
        extra = '\n\n| Pooled | Total |\n| --- | --- |\n| All | 199/199 |\n'
        for prefix in ('<!-- harmless -->```', '<!-- harmless -->~~~', '``` <!--\ncode\n```'):
            with self.subTest(prefix=prefix):
                docs = self.docs.copy()
                docs['index'] += '\n\n' + prefix + extra
                with self.assertRaisesRegex(ValueError, 'result table|raw HTML'):
                    report.check_docs(self.rendered, docs)
        docs = self.docs.copy()
        table = self.rendered['index']
        docs['index'] = docs['index'].replace(table, '<!-- harmless -->' + table)
        with self.assertRaisesRegex(ValueError, 'raw HTML'):
            report.check_docs(self.rendered, docs)

    def test_rejects_unsupported_raw_html_around_tables(self):
        for opening, closing in (('<div>', '</div>'), ('<pre>', '</pre>'),
                                  ('<script>', '</script>'), ('<div\nclass="hidden">', '</div>'),
                                  ('<pre>\n', '\n</pre>'), ('<style>\n', '\n</style>')):
            with self.subTest(opening=opening):
                docs = self.docs.copy()
                table = self.rendered['index']
                docs['index'] = docs['index'].replace(table, f'{opening}\n{table}\n{closing}')
                with self.assertRaisesRegex(ValueError, 'unsupported raw HTML'):
                    report.check_docs(self.rendered, docs)

    def test_rejects_second_evidence_mode_basis(self):
        self.definitions['R3']['requirements'][0]['mode'] = 'semantic'
        for row in self.attempts:
            if row['case_id'] == 'R3':
                row['requirements'][0]['mode'] = 'semantic'
        self.summary['evidence_coverage']['objective']['pass'] -= 6
        self.summary['evidence_coverage']['semantic']['pass'] += 6
        with self.assertRaisesRegex(ValueError, 'evidence basis'):
            self.validate()

    def test_rejects_changed_index_counts_units_and_arms(self):
        for old, new in (('4 / 24', '24 / 24'), ('8 / 16', '9 / 16'),
                         ('40/40', '39/40'), ('159/159', '199/199'),
                         ('criterion groups', 'requirements'), ('8 tied', '16 tied'),
                         ('| With skill | Baseline |', '| Baseline | With skill |')):
            with self.subTest(mutation=(old, new)):
                docs = self.docs.copy()
                docs['index'] = docs['index'].replace(old, new)
                with self.assertRaisesRegex(ValueError, 'result table'):
                    report.check_docs(self.rendered, docs)

    def test_rejects_changed_evidence_mode_counts_and_labels(self):
        for old, new in (('204/204', '204/318'), ('36/36', '72/72'),
                         ('| Mechanical |', '| Behavioral |'),
                         ('AI-assisted semantic', 'Human-rated semantic')):
            with self.subTest(mutation=(old, new)):
                docs = self.docs.copy()
                docs['study'] = docs['study'].replace(old, new)
                with self.assertRaisesRegex(ValueError, 'result table'):
                    report.check_docs(self.rendered, docs)

    def test_rejects_changed_submission_identity_outcomes_and_links(self):
        first = self.rendered['attempts'].splitlines()[2]
        for old, new in (('| R3 |', '| R1 |'), ('| 1 |', '| 2 |'), ('| S |', '| C |'),
                         ('12 / 12', '12 / 14'), ('| 0 | 0 |', '| 1 | 0 |'),
                         ('| 0 | 0 |', '| 0 | 1 |'),
                         ('../artifacts/T01-R3-r1-S/', '../artifacts/T02-R3-r1-C/')):
            with self.subTest(mutation=(old, new)):
                docs = self.docs.copy()
                docs['attempts'] = docs['attempts'].replace(first, first.replace(old, new))
                with self.assertRaisesRegex(ValueError, 'result table'):
                    report.check_docs(self.rendered, docs)

    def test_rejects_ledger_json_out_of_dispatch_order(self):
        self.attempts.reverse()
        with self.assertRaisesRegex(ValueError, 'dispatch order'):
            self.validate()

    def test_rejects_duplicate_scheduled_dispatch_index(self):
        self.schedule['attempts'][1]['dispatch_index'] = 1
        with self.assertRaisesRegex(ValueError, 'dispatch index'):
            self.validate()

    def test_rejects_stale_attempt_dispatch_index(self):
        self.attempts[0]['dispatch_index'] = 2
        with self.assertRaisesRegex(ValueError, 'dispatch index mismatch'):
            self.validate()

    def test_rejects_duplicate_summary_case(self):
        self.summary['cases'].append(copy.deepcopy(self.summary['cases'][0]))
        with self.assertRaisesRegex(ValueError, 'summary case'):
            self.validate()

    def test_rejects_stale_case_denominator(self):
        self.summary['cases'][0]['requirements_per_attempt'] += 1
        with self.assertRaisesRegex(ValueError, 'case label or denominator'):
            self.validate()

    def test_rejects_stale_case_count(self):
        self.summary['cases'][0]['conditions']['S']['counts']['pass'] -= 1
        with self.assertRaisesRegex(ValueError, 'stale case counts'):
            self.validate()

    def test_rejects_duplicate_requirement_with_unchanged_counts(self):
        self.attempts[0]['requirements'][-1] = copy.deepcopy(self.attempts[0]['requirements'][0])
        with self.assertRaisesRegex(ValueError, 'requirement identity or evidence mode'):
            self.validate()

    def test_rejects_swapped_requirement_mode_with_unchanged_outcomes(self):
        self.attempts[0]['requirements'][0]['mode'] = 'semantic'
        with self.assertRaisesRegex(ValueError, 'requirement identity or evidence mode'):
            self.validate()

    def test_rejects_stale_evidence_coverage(self):
        self.summary['evidence_coverage']['semantic']['pass'] *= 2
        with self.assertRaisesRegex(ValueError, 'evidence-mode counts'):
            self.validate()

    def test_evidence_denominator_retains_failed_and_not_assessed(self):
        self.summary['evidence_coverage']['semantic'] = {'pass': 30, 'fail': 4, 'not_assessed': 2}
        rendered = report.tables(self.summary, self.attempts, self.initial)
        self.assertIn('| AI-assisted semantic | 30/36 |', rendered['evidence'])

    def test_rejects_stale_paired_outcomes(self):
        self.summary['pairs'][0]['verified_pass_difference_S_minus_C'] = 1
        with self.assertRaisesRegex(ValueError, 'paired outcomes'):
            self.validate()

    def test_rejects_cross_attempt_and_duplicate_artifact_links(self):
        for path in ('artifacts/T02-R3-r1-C/notes.md', 'artifacts/T01-R3-r1-S/../notes.md',
                     self.attempts[0]['artifacts'][1]['path']):
            with self.subTest(path=path):
                self.attempts[0]['artifacts'][0]['path'] = path
                with self.assertRaisesRegex(ValueError, 'artifact links'):
                    self.validate()

    def test_rejects_stale_distinct_requirement_and_file_totals(self):
        for key in ('distinct_requirements', 'artifact_files'):
            with self.subTest(key=key):
                self.summary[key] += 1
                with self.assertRaisesRegex(ValueError, 'stale .* count'):
                    self.validate()
                self.summary[key] -= 1

    def test_rejects_initial_missing_or_duplicate_attempt(self):
        self.initial_attempts['rows'].pop()
        with self.assertRaisesRegex(ValueError, 'initial scheduled attempt'):
            self.validate_initial()
        self.initial_attempts['rows'].append(copy.deepcopy(self.initial_attempts['rows'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate initial attempt'):
            self.validate_initial()

    def test_rejects_initial_duplicate_case(self):
        self.initial['rows'][-1] = copy.deepcopy(self.initial['rows'][0])
        with self.assertRaisesRegex(ValueError, 'initial case'):
            self.validate_initial()

    def test_rejects_initial_wrong_case_and_condition_counts(self):
        self.initial['scheduled_cases'] += 1
        with self.assertRaisesRegex(ValueError, 'case or attempt count'):
            self.validate_initial()
        self.initial['scheduled_cases'] -= 1
        self.initial['C']['passed'] += 1
        with self.assertRaisesRegex(ValueError, 'initial condition counts'):
            self.validate_initial()

    def test_initial_asymmetric_counts_keep_arm_mapping(self):
        row = next(row for row in self.initial_attempts['rows'] if row['arm'] == 'S')
        row['criterion_groups'][0]['passed'] = False
        pair = next(pair for pair in self.initial['rows'] if pair['case_id'] == row['case_id'])
        pair['S'].update(passed=4, failed=1)
        pair.update(S_minus_C_passed_groups=-1, paired_outcome='S_loss')
        self.initial['S'].update(passed=39, failed=1)
        self.initial['paired_outcomes'].update(tie=7, S_loss=1)
        self.validate_initial()
        rendered = report.tables(self.summary, self.attempts, self.initial)
        self.assertIn('| 39/40 criterion groups | 40/40 criterion groups | 7 tied case pairs |', rendered['index'])
        for attempt in self.initial_attempts['rows']:
            if attempt['case_id'] == row['case_id']:
                attempt['arm'] = 'C' if attempt['arm'] == 'S' else 'S'
        with self.assertRaisesRegex(ValueError, 'identity or schedule mismatch'):
            self.validate_initial()

    def test_rejects_equal_tie_initial_arm_relabeling(self):
        for row in self.initial_attempts['rows']:
            row['arm'] = 'S' if row['arm'] == 'C' else 'C'
        with self.assertRaisesRegex(ValueError, 'identity or schedule mismatch'):
            self.validate_initial()

    def test_rejects_initial_case_and_ordinal_relabeling(self):
        row = self.initial_attempts['rows'][0]
        for key, value in (('case_id', 'F1'), ('schedule_ordinal', 2), ('schedule_ordinal', True)):
            with self.subTest(key=key, value=value):
                original = row[key]
                row[key] = value
                with self.assertRaisesRegex(ValueError, 'identity or schedule mismatch'):
                    self.validate_initial()
                row[key] = original

    def test_rejects_changed_numeric_prose(self):
        for name, old, new in (('overview', 'Cases: 4', 'Cases: 24'),
                               ('study', '318 scheduled', '398 scheduled'),
                               ('index', '[all 16 attempts]', '[all 18 attempts]'),
                               ('attempts', 'All 24 rows', 'All 23 rows')):
            with self.subTest(document=name):
                docs = self.docs.copy()
                docs[name] = docs[name].replace(old, new)
                with self.assertRaisesRegex(ValueError, 'numeric statement'):
                    report.check_claims(self.summary, self.attempts, self.initial, docs)

    def test_rejects_positive_pooling_or_process_claim_replacements(self):
        for name, old, new in (('index', 'Do not pool their denominators.', 'Pool their denominators.'),
                               ('overview', 'Its scores are not pooled', 'Its scores are pooled'),
                               ('study', 'Its denominators are not pooled', 'Its denominators are pooled'),
                               ('attempts', 'Process integrity is unknown', 'Process integrity is verified')):
            with self.subTest(document=name):
                docs = self.docs.copy()
                docs[name] = docs[name].replace(old, new)
                with self.assertRaisesRegex(ValueError, 'condition definition or limitation'):
                    report.check_docs(self.rendered, docs)

    def test_rejects_unsupported_ceiling_prose(self):
        self.attempts[0]['counts'].update({'pass': 11, 'not_assessed': 1})
        with self.assertRaisesRegex(ValueError, 'ceiling and all-pairs-tied prose'):
            report.check_claims(self.summary, self.attempts, self.initial, self.docs)


if __name__ == '__main__':
    unittest.main()
