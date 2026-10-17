import unittest

from rights_classifier import (
    CommercialUseClass,
    LayerAssessment,
    LayerStatus,
    classify,
    status_from_license,
)


E1 = ("https://example.invalid/evidence/work",)
E2 = ("https://example.invalid/evidence/edition",)


class RightsClassifierTests(unittest.TestCase):
    def test_a_requires_both_layers_open_and_evidence(self):
        decision = classify(
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL, E1),
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL, E2),
        )
        self.assertEqual(CommercialUseClass.A, decision.commercial_use_class)
        self.assertFalse(decision.manual_review_required)

    def test_missing_evidence_in_both_layers_degrades_to_e(self):
        decision = classify(
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL),
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL),
        )
        self.assertEqual(CommercialUseClass.E, decision.commercial_use_class)
        self.assertTrue(decision.manual_review_required)

    def test_underlying_missing_evidence_degrades_to_e_even_if_edition_has_evidence(self):
        decision = classify(
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL),
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL, E2),
        )
        self.assertEqual(CommercialUseClass.E, decision.commercial_use_class)
        self.assertTrue(decision.manual_review_required)
        self.assertIn("Underlying work", decision.blocking_reason)

    def test_edition_missing_evidence_degrades_to_e_even_if_underlying_has_evidence(self):
        decision = classify(
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL, E1),
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL),
        )
        self.assertEqual(CommercialUseClass.E, decision.commercial_use_class)
        self.assertTrue(decision.manual_review_required)
        self.assertIn("edition/file", decision.blocking_reason)

    def test_blank_evidence_url_does_not_satisfy_layer_requirement(self):
        decision = classify(
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL, ("   ",)),
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL, E2),
        )
        self.assertEqual(CommercialUseClass.E, decision.commercial_use_class)
        self.assertTrue(decision.manual_review_required)

    def test_edition_status_without_evidence_cannot_produce_b_c_or_d(self):
        cases = (
            LayerStatus.COMMERCIAL_WITH_CONDITIONS,
            LayerStatus.NONCOMMERCIAL_ONLY,
            LayerStatus.RIGHTS_RESERVED_OR_PERMISSION_REQUIRED,
        )

        for status in cases:
            with self.subTest(status=status):
                decision = classify(
                    LayerAssessment(LayerStatus.OPEN_COMMERCIAL, E1),
                    LayerAssessment(status),
                )
                self.assertEqual(
                    CommercialUseClass.E,
                    decision.commercial_use_class,
                )
                self.assertTrue(decision.manual_review_required)
                self.assertIn("edition/file", decision.blocking_reason)

    def test_underlying_status_without_evidence_cannot_produce_b_c_or_d(self):
        cases = (
            LayerStatus.COMMERCIAL_WITH_CONDITIONS,
            LayerStatus.NONCOMMERCIAL_ONLY,
            LayerStatus.RIGHTS_RESERVED_OR_PERMISSION_REQUIRED,
        )

        for status in cases:
            with self.subTest(status=status):
                decision = classify(
                    LayerAssessment(status),
                    LayerAssessment(LayerStatus.OPEN_COMMERCIAL, E2),
                )
                self.assertEqual(
                    CommercialUseClass.E,
                    decision.commercial_use_class,
                )
                self.assertTrue(decision.manual_review_required)
                self.assertIn("Underlying work", decision.blocking_reason)

    def test_uncertain_layer_always_degrades_to_e(self):
        decision = classify(
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL, E1),
            LayerAssessment(LayerStatus.UNCERTAIN, E2),
        )
        self.assertEqual(CommercialUseClass.E, decision.commercial_use_class)

    def test_reserved_rights_produces_d(self):
        decision = classify(
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL, E1),
            LayerAssessment(
                LayerStatus.RIGHTS_RESERVED_OR_PERMISSION_REQUIRED, E2
            ),
        )
        self.assertEqual(CommercialUseClass.D, decision.commercial_use_class)

    def test_noncommercial_layer_produces_c(self):
        decision = classify(
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL, E1),
            LayerAssessment(LayerStatus.NONCOMMERCIAL_ONLY, E2),
        )
        self.assertEqual(CommercialUseClass.C, decision.commercial_use_class)

    def test_conditional_layer_produces_b(self):
        decision = classify(
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL, E1),
            LayerAssessment(LayerStatus.COMMERCIAL_WITH_CONDITIONS, E2),
        )
        self.assertEqual(CommercialUseClass.B, decision.commercial_use_class)

    def test_public_domain_work_modern_reserved_edition_is_d(self):
        decision = classify(
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL, E1),
            LayerAssessment(
                LayerStatus.RIGHTS_RESERVED_OR_PERMISSION_REQUIRED, E2
            ),
        )
        self.assertEqual(CommercialUseClass.D, decision.commercial_use_class)

    def test_medium_confidence_still_requires_manual_review(self):
        decision = classify(
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL, E1),
            LayerAssessment(LayerStatus.OPEN_COMMERCIAL, E2),
            confidence="MEDIUM",
        )
        self.assertEqual(CommercialUseClass.A, decision.commercial_use_class)
        self.assertTrue(decision.manual_review_required)

    def test_license_mapping(self):
        self.assertEqual(
            LayerStatus.COMMERCIAL_WITH_CONDITIONS,
            status_from_license("CC-BY-SA"),
        )
        self.assertEqual(
            LayerStatus.NONCOMMERCIAL_ONLY,
            status_from_license("CC-BY-NC"),
        )
        self.assertEqual(
            LayerStatus.UNCERTAIN,
            status_from_license("unknown"),
        )


if __name__ == "__main__":
    unittest.main()
