"""
POS Scope Analyzer - Intelligent scope analysis for POS quote generation.
Analyzes construction scopes and generates multiple quote options with matched activities.
"""

import re
import os
from typing import Dict, List, Tuple
from decimal import Decimal

# Try to import OpenAI for enhanced analysis
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class POSAnalyzer:
    """
    Analyzes construction project scopes and generates intelligent quote options
    by matching scope text to POS categories and activities.
    """

    def __init__(self):
        self.use_openai = False
        if OPENAI_AVAILABLE:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                openai.api_key = api_key
                self.use_openai = True
                print("[POS Analyzer] OpenAI integration enabled")
            else:
                print("[POS Analyzer] Using rule-based analysis (no OpenAI key)")
        else:
            print("[POS Analyzer] Using rule-based analysis (OpenAI not installed)")

    def analyze_scope_and_generate_options(
        self,
        scope_text: str,
        all_categories: List[Dict],
        budget_hint: Decimal = None
    ) -> Dict:
        """
        Main analysis function: analyzes scope and generates 3 quote options.

        Args:
            scope_text: Raw scope of work description
            all_categories: List of all available POS categories with activities
            budget_hint: Optional budget hint to calibrate pricing tiers

        Returns:
            Dictionary with analysis results and 3 quote options (basic, standard, premium)
        """

        # Step 1: Analyze the scope
        analysis = self._analyze_scope(scope_text)

        # Step 2: Match categories and activities
        matched_items = self._match_activities_to_scope(
            analysis,
            all_categories
        )

        # Step 3: Generate 3 pricing tiers
        options = self._generate_quote_options(
            matched_items,
            analysis,
            budget_hint
        )

        return {
            'analysis': analysis,
            'matched_items': matched_items,
            'options': options
        }

    def _analyze_scope(self, scope_text: str) -> Dict:
        """
        Analyze scope text to extract key information.

        Returns:
            Dictionary with project_type, locations, work_items, materials, complexity
        """

        if self.use_openai:
            return self._analyze_with_openai(scope_text)
        else:
            return self._analyze_rule_based(scope_text)

    def _analyze_with_openai(self, scope_text: str) -> Dict:
        """Use OpenAI to analyze scope"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": """You are a construction estimator. Analyze the scope carefully and extract all numerical measurements.

Return JSON with:
{
    "project_type": "specific type (kitchen, bathroom, flooring, roofing, etc)",
    "locations": ["list", "of", "locations"],
    "work_items": ["specific", "work", "tasks"],
    "materials": ["materials", "mentioned"],
    "complexity": 1-5,
    "estimated_days": number,
    "square_footage": number (extract total sq ft, sqft, square feet mentioned - if none found use 0),
    "linear_footage": number (extract linear ft, lf mentioned - if none found use 0)
}

IMPORTANT: Extract any numbers followed by "sq ft", "sqft", "square feet", "sf" and sum them for square_footage.
Extract any numbers followed by "linear ft", "lf", "linear feet" for linear_footage.
Be aggressive in finding these measurements - they are critical for accurate quoting."""
                }, {
                    "role": "user",
                    "content": f"Analyze this construction scope: {scope_text}"
                }],
                temperature=0.3
            )

            import json
            analysis = json.loads(response.choices[0].message.content)
            analysis['llm_processed'] = True

            # Ensure square_footage and linear_footage are present
            if 'square_footage' not in analysis:
                analysis['square_footage'] = 0
            if 'linear_footage' not in analysis:
                analysis['linear_footage'] = 0

            return analysis

        except Exception as e:
            print(f"[POS Analyzer] OpenAI error: {e}, falling back to rule-based")
            return self._analyze_rule_based(scope_text)

    def _analyze_rule_based(self, scope_text: str) -> Dict:
        """Rule-based scope analysis (fallback or standalone)"""
        scope_lower = scope_text.lower()

        # Extract project type
        project_type = self._extract_project_type(scope_lower)

        # Extract locations
        locations = self._extract_locations(scope_lower)

        # Extract work items using verb patterns
        work_items = self._extract_work_items(scope_text)

        # Extract materials
        materials = self._extract_materials(scope_lower)

        # Extract measurements
        square_footage = self._extract_square_footage(scope_text)
        linear_footage = self._extract_linear_footage(scope_text)

        # Calculate complexity (1-5)
        complexity = self._calculate_complexity(scope_lower, work_items)

        # Estimate timeline
        estimated_days = self._estimate_timeline(complexity, len(work_items))

        return {
            'project_type': project_type,
            'locations': locations,
            'work_items': work_items,
            'materials': materials,
            'complexity': complexity,
            'estimated_days': estimated_days,
            'square_footage': square_footage,
            'linear_footage': linear_footage,
            'llm_processed': False
        }

    def _extract_project_type(self, scope_lower: str) -> str:
        """Identify primary project type"""
        project_indicators = {
            'kitchen': ['kitchen', 'cabinet', 'countertop', 'appliance'],
            'bathroom': ['bathroom', 'bath', 'shower', 'toilet', 'vanity'],
            'roofing': ['roof', 'shingle', 'gutter', 'flashing'],
            'flooring': ['floor', 'carpet', 'hardwood', 'tile', 'laminate'],
            'painting': ['paint', 'color', 'primer', 'wall'],
            'plumbing': ['plumb', 'pipe', 'water', 'drain'],
            'electrical': ['electric', 'wire', 'outlet', 'circuit'],
            'siding': ['siding', 'exterior', 'cladding'],
            'deck': ['deck', 'patio', 'outdoor', 'pergola']
        }

        scores = {}
        for proj_type, keywords in project_indicators.items():
            score = sum(1 for keyword in keywords if keyword in scope_lower)
            if score > 0:
                scores[proj_type] = score

        if scores:
            return max(scores, key=scores.get)
        return 'general renovation'

    def _extract_locations(self, scope_lower: str) -> List[str]:
        """Extract locations mentioned"""
        locations = {
            'Kitchen': ['kitchen'],
            'Master Bathroom': ['master bath'],
            'Bathroom': ['bathroom', 'bath'],
            'Living Room': ['living room', 'family room'],
            'Bedroom': ['bedroom'],
            'Basement': ['basement'],
            'Exterior': ['exterior', 'outside']
        }

        detected = []
        for location, keywords in locations.items():
            if any(kw in scope_lower for kw in keywords):
                detected.append(location)

        return detected if detected else ['General Areas']

    def _extract_work_items(self, scope_text: str) -> List[str]:
        """Extract specific work items using verb patterns"""
        patterns = [
            (r'install\s+([^.,\n]+)', 'Install'),
            (r'replace\s+([^.,\n]+)', 'Replace'),
            (r'repair\s+([^.,\n]+)', 'Repair'),
            (r'remove\s+([^.,\n]+)', 'Remove'),
            (r'paint\s+([^.,\n]+)', 'Paint'),
            (r'renovate\s+([^.,\n]+)', 'Renovate'),
            (r'update\s+([^.,\n]+)', 'Update'),
            (r'add\s+([^.,\n]+)', 'Add'),
        ]

        work_items = []
        for pattern, action in patterns:
            matches = re.findall(pattern, scope_text, re.IGNORECASE)
            for match in matches:
                item = f"{action} {match.strip()}"
                if len(item) < 80:
                    work_items.append(item)

        return work_items

    def _extract_materials(self, scope_lower: str) -> List[str]:
        """Extract materials mentioned"""
        materials_list = [
            'cabinets', 'countertops', 'appliances', 'tile', 'hardwood',
            'carpet', 'paint', 'fixtures', 'granite', 'quartz',
            'drywall', 'flooring', 'doors', 'windows', 'shingles',
            'siding', 'deck boards', 'railing', 'vanity', 'shower'
        ]

        detected = []
        for material in materials_list:
            if material in scope_lower:
                detected.append(material.title())

        return detected

    def _extract_square_footage(self, scope_text: str) -> int:
        """Extract square footage from scope text using regex"""
        # Patterns to match various square footage formats
        patterns = [
            r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:sq\.?\s*ft|sqft|square\s+feet?|sf)\b',
            r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:sq\s+ft|square\s+foot)',
        ]

        total_sqft = 0
        for pattern in patterns:
            matches = re.findall(pattern, scope_text, re.IGNORECASE)
            for match in matches:
                # Remove commas and convert to float
                sqft = float(match.replace(',', ''))
                total_sqft += sqft

        return int(total_sqft)

    def _extract_linear_footage(self, scope_text: str) -> int:
        """Extract linear footage from scope text using regex"""
        # Patterns to match various linear footage formats
        patterns = [
            r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:linear\s+ft|linear\s+feet?|lf)\b',
            r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:lin\.?\s*ft|lineal\s+feet?)',
        ]

        total_lf = 0
        for pattern in patterns:
            matches = re.findall(pattern, scope_text, re.IGNORECASE)
            for match in matches:
                # Remove commas and convert to float
                lf = float(match.replace(',', ''))
                total_lf += lf

        return int(total_lf)

    def _calculate_complexity(self, scope_lower: str, work_items: List[str]) -> int:
        """Calculate complexity score 1-5"""
        complexity_indicators = {
            5: ['structural', 'addition', 'new construction', 'gut'],
            4: ['major renovation', 'move wall', 'rewire', 'replumb'],
            3: ['remodel', 'renovation', 'multiple'],
            2: ['replace', 'install', 'update'],
            1: ['paint', 'repair', 'minor', 'touch up']
        }

        max_complexity = 1
        for level, keywords in complexity_indicators.items():
            if any(kw in scope_lower for kw in keywords):
                max_complexity = max(max_complexity, level)

        # Adjust based on number of work items
        if len(work_items) > 10:
            max_complexity = min(5, max_complexity + 1)
        elif len(work_items) > 5:
            max_complexity = min(5, max_complexity)

        return max_complexity

    def _estimate_timeline(self, complexity: int, work_item_count: int) -> int:
        """Estimate project timeline in days"""
        base_days = {1: 3, 2: 7, 3: 14, 4: 21, 5: 45}
        return base_days[complexity] + (work_item_count * 1)

    def _match_activities_to_scope(
        self,
        analysis: Dict,
        all_categories: List[Dict]
    ) -> List[Dict]:
        """
        Match POS activities to the analyzed scope.

        Returns:
            List of matched activities with suggested quantities
        """

        matched_items = []
        project_type = analysis['project_type']
        work_items = analysis['work_items']
        materials = analysis['materials']
        scope_keywords = set(project_type.lower().split() +
                           [item.lower() for item in materials])

        for category in all_categories:
            # Check if category is relevant
            category_keywords = set(category.get('keywords', '').lower().split(','))
            category_keywords = {kw.strip() for kw in category_keywords if kw.strip()}

            if scope_keywords & category_keywords:
                # Category matches, check activities
                for activity in category.get('activities', []):
                    activity_name = activity['name'].lower()

                    # Check if activity matches work items or materials
                    relevance_score = 0
                    for work_item in work_items:
                        if any(word in activity_name for word in work_item.lower().split()):
                            relevance_score += 2

                    for material in materials:
                        if material.lower() in activity_name:
                            relevance_score += 1

                    if relevance_score > 0:
                        matched_items.append({
                            'category_id': category['id'],
                            'category_name': category['name'],
                            'activity_id': activity['id'],
                            'activity_name': activity['name'],
                            'base_cost': activity['base_cost'],
                            'unit': activity['unit'],
                            'relevance_score': relevance_score,
                            'suggested_quantity': self._suggest_quantity(
                                activity,
                                analysis
                            )
                        })

        # Sort by relevance
        matched_items.sort(key=lambda x: x['relevance_score'], reverse=True)

        return matched_items[:15]  # Top 15 most relevant

    def _suggest_quantity(self, activity: Dict, analysis: Dict) -> Decimal:
        """Suggest quantity based on activity unit and scope"""
        unit = activity.get('unit', 'each')
        complexity = analysis.get('complexity', 3)

        # Use extracted measurements if available
        square_footage = analysis.get('square_footage', 0)
        linear_footage = analysis.get('linear_footage', 0)

        # If we have actual measurements, use them
        if unit == 'sqft' and square_footage > 0:
            return Decimal(str(square_footage))
        elif unit == 'linear_ft' and linear_footage > 0:
            return Decimal(str(linear_footage))

        # Otherwise, use default quantities based on unit type and complexity
        quantity_map = {
            'each': Decimal('1'),
            'sqft': Decimal(str(100 * complexity)),  # Fallback: More complex = more sq ft
            'linear_ft': Decimal(str(20 * complexity)),  # Fallback
            'hour': Decimal(str(8 * complexity)),
        }

        return quantity_map.get(unit, Decimal('1'))

    def _generate_quote_options(
        self,
        matched_items: List[Dict],
        analysis: Dict,
        budget_hint: Decimal = None
    ) -> List[Dict]:
        """
        Generate 3 quote options: Basic, Standard, Premium

        Returns:
            List of 3 option dictionaries with items and totals
        """

        if not matched_items:
            return []

        # Separate items into must-have and optional
        must_have = matched_items[:5]  # Top 5 most relevant
        optional = matched_items[5:10]  # Next 5
        premium_extras = matched_items[10:15]  # Additional premium items

        # Option 1: Basic (essential items only)
        basic_items = self._build_option_items(must_have, tier='basic')
        basic_total = sum(item['total_cost'] for item in basic_items)

        # Option 2: Standard (essential + some optional)
        standard_items = self._build_option_items(
            must_have + optional[:3],
            tier='standard'
        )
        standard_total = sum(item['total_cost'] for item in standard_items)

        # Option 3: Premium (all items + extras)
        premium_items = self._build_option_items(
            must_have + optional + premium_extras,
            tier='premium'
        )
        premium_total = sum(item['total_cost'] for item in premium_items)

        return [
            {
                'tier': 'Basic',
                'description': 'Essential work to complete the project',
                'items': basic_items,
                'total': float(basic_total),
                'timeline_days': analysis.get('estimated_days', 14)
            },
            {
                'tier': 'Standard',
                'description': 'Recommended option with quality upgrades',
                'items': standard_items,
                'total': float(standard_total),
                'timeline_days': int(analysis.get('estimated_days', 14) * 1.2)
            },
            {
                'tier': 'Premium',
                'description': 'Complete transformation with premium finishes',
                'items': premium_items,
                'total': float(premium_total),
                'timeline_days': int(analysis.get('estimated_days', 14) * 1.4)
            }
        ]

    def _build_option_items(self, matched_items: List[Dict], tier: str) -> List[Dict]:
        """Build list of items for a specific pricing tier"""
        tier_multipliers = {
            'basic': Decimal('0.85'),      # 15% discount for basic materials
            'standard': Decimal('1.0'),    # Standard pricing
            'premium': Decimal('1.25')     # 25% markup for premium materials
        }

        multiplier = tier_multipliers.get(tier, Decimal('1.0'))
        items = []

        for matched_item in matched_items:
            quantity = matched_item['suggested_quantity']
            base_cost = Decimal(str(matched_item['base_cost']))
            adjusted_cost = base_cost * multiplier
            total_cost = adjusted_cost * quantity

            items.append({
                'activity_id': matched_item['activity_id'],
                'activity_name': matched_item['activity_name'],
                'category_name': matched_item['category_name'],
                'quantity': float(quantity),
                'unit': matched_item['unit'],
                'unit_cost': float(adjusted_cost),
                'total_cost': float(total_cost),
                'tier': tier
            })

        return items


def create_pos_analyzer():
    """Factory function to create analyzer instance"""
    return POSAnalyzer()
