"""Menu data and search functionality."""
from app.models.schemas import MenuItem


class MenuService:
    """Service for managing menu data."""

    def __init__(self):
        """Initialize menu service with restaurant menu."""
        self.menu = self._load_menu()

    def _load_menu(self) -> list[MenuItem]:
        """Load the restaurant menu."""
        return [
            # Starters
            MenuItem(
                id="tandoori_lamb_chops",
                name="Tandoori Lamb Chops",
                description="Succulent lamb chops marinated in yogurt and spices, cooked in clay oven",
                price=14.99,
                category="Starters",
                dietary_tags=["GF"],
            ),
            MenuItem(
                id="samosas",
                name="Vegetable Samosas",
                description="Crispy pastry pockets filled with spiced potato, peas, and onions",
                price=5.99,
                category="Starters",
                dietary_tags=["V"],
            ),
            MenuItem(
                id="paneer_tikka",
                name="Paneer Tikka",
                description="Cubes of cottage cheese marinated and grilled with peppers and onions",
                price=8.99,
                category="Starters",
                dietary_tags=["V", "GF"],
            ),
            MenuItem(
                id="seekh_kebab",
                name="Chicken Seekh Kebab",
                description="Minced chicken mixed with spices, formed on skewers and chargrilled",
                price=9.99,
                category="Starters",
                dietary_tags=["GF"],
            ),
            MenuItem(
                id="onion_bhaji",
                name="Onion Bhaji",
                description="Crispy fried onion fritters with a light gram flour batter",
                price=4.99,
                category="Starters",
                dietary_tags=["V"],
            ),
            # Mains
            MenuItem(
                id="butter_chicken",
                name="Butter Chicken",
                description="Tender chicken in a creamy tomato and butter sauce with aromatic spices",
                price=12.99,
                category="Mains",
            ),
            MenuItem(
                id="kerala_fish_curry",
                name="Kerala Fish Curry",
                description="Fresh fish cooked in coconut milk with curry leaves and tamarind",
                price=15.99,
                category="Mains",
                dietary_tags=["GF"],
            ),
            MenuItem(
                id="lamb_rogan_josh",
                name="Lamb Rogan Josh",
                description="Tender pieces of lamb in a rich and aromatic tomato-based curry",
                price=14.99,
                category="Mains",
                dietary_tags=["GF"],
            ),
            MenuItem(
                id="chana_masala",
                name="Chana Masala",
                description="Spiced chickpeas cooked with tomatoes, onions, and traditional spices",
                price=9.99,
                category="Mains",
                dietary_tags=["V", "VG", "GF"],
            ),
            MenuItem(
                id="palak_paneer",
                name="Palak Paneer",
                description="Cottage cheese cubes in a creamy spinach sauce",
                price=10.99,
                category="Mains",
                dietary_tags=["V", "GF"],
            ),
            MenuItem(
                id="prawn_karahi",
                name="Prawn Karahi",
                description="Succulent prawns tossed with peppers, tomatoes, and aromatic spices",
                price=16.99,
                category="Mains",
                dietary_tags=["GF"],
            ),
            # Sides
            MenuItem(
                id="naan_plain",
                name="Plain Naan",
                description="Soft, fluffy Indian bread baked in clay oven",
                price=2.99,
                category="Sides",
                dietary_tags=["V"],
            ),
            MenuItem(
                id="garlic_naan",
                name="Garlic Naan",
                description="Naan topped with fresh garlic and herbs",
                price=3.99,
                category="Sides",
                dietary_tags=["V"],
            ),
            MenuItem(
                id="masala_chips",
                name="Masala Chips",
                description="Hand-cut fries sprinkled with chat masala spices",
                price=4.99,
                category="Sides",
                dietary_tags=["V", "GF"],
            ),
            MenuItem(
                id="basmati_rice",
                name="Fragrant Basmati Rice",
                description="Fluffy long-grain basmati rice",
                price=3.99,
                category="Sides",
                dietary_tags=["V", "VG", "GF"],
            ),
            # Desserts
            MenuItem(
                id="chai_brulee",
                name="Chai Crème Brûlée",
                description="Silky custard infused with chai spices, topped with caramelized sugar",
                price=6.99,
                category="Desserts",
                dietary_tags=["V"],
            ),
            MenuItem(
                id="gulab_jamun",
                name="Gulab Jamun",
                description="Soft milk solids pastry balls soaked in sugar syrup with cardamom",
                price=5.99,
                category="Desserts",
                dietary_tags=["V"],
            ),
            MenuItem(
                id="mango_lassi",
                name="Mango Lassi",
                description="Refreshing yogurt-based drink with fresh mango and cardamom",
                price=4.99,
                category="Beverages",
                dietary_tags=["V"],
            ),
            MenuItem(
                id="masala_chai",
                name="Masala Chai",
                description="Traditional spiced tea with milk and cardamom",
                price=2.99,
                category="Beverages",
                dietary_tags=["V"],
            ),
        ]

    def get_all_items(self) -> list[MenuItem]:
        """Get all menu items."""
        return self.menu

    def get_items_by_category(self, category: str) -> list[MenuItem]:
        """Get menu items by category."""
        return [item for item in self.menu if item.category.lower() == category.lower()]

    def search_items(self, query: str) -> list[MenuItem]:
        """Search menu items by name or description."""
        query_lower = query.lower()
        return [
            item
            for item in self.menu
            if query_lower in item.name.lower() or query_lower in item.description.lower()
        ]

    def get_item_by_id(self, item_id: str) -> MenuItem | None:
        """Get a menu item by ID."""
        for item in self.menu:
            if item.id == item_id:
                return item
        return None

    def get_categories(self) -> list[str]:
        """Get all unique menu categories."""
        return list(set(item.category for item in self.menu))

    def get_vegetarian_items(self) -> list[MenuItem]:
        """Get all vegetarian items."""
        return [item for item in self.menu if "V" in item.dietary_tags or "VG" in item.dietary_tags]

    def get_gluten_free_items(self) -> list[MenuItem]:
        """Get all gluten-free items."""
        return [item for item in self.menu if "GF" in item.dietary_tags]
