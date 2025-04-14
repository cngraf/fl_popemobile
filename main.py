"""
Main entry point for the Fallen London optimization tool.

This module provides the core functionality for running the optimization system,
including module registration, configuration management, and the main execution
flow. It uses a modular architecture to support various game mechanics and
locations through separate trade modules.

The system is designed to be extensible, allowing new trade modules to be added
without modifying the core optimization logic.
"""

from config import *
from enums import *
from helper.utils import *
from optimization.model_runner import *
from optimization.config_manager import ConfigManager
import logging
from pathlib import Path
import importlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModuleRegistry:
    """
    Registry for managing trade modules in the optimization system.
    
    This class provides a centralized mechanism for loading and managing trade
    modules, which define various game mechanics and locations. It supports
    dynamic loading of modules and provides error handling for module registration.
    
    Attributes:
        modules (list): List of successfully loaded trade modules
    """
    
    def __init__(self):
        """Initialize an empty module registry."""
        self.modules = []
    
    def register_module(self, module_name: str):
        """
        Register a trade module by its import path.
        
        This method attempts to import and register a module, checking for the
        presence of the required add_trades function. If successful, the module
        is added to the registry; if not, an error is logged.
        
        Args:
            module_name (str): The import path of the module to register
        """
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, 'add_trades'):
                self.modules.append(module)
                logger.info(f"Registered module: {module_name}")
            else:
                logger.warning(f"Module {module_name} does not have add_trades function")
        except ImportError as e:
            logger.error(f"Failed to import module {module_name}: {e}")
    
    def add_trades(self, config: Config):
        """
        Add trades from all registered modules to the configuration.
        
        This method iterates through all registered modules and calls their
        add_trades function to register their trades with the configuration.
        
        Args:
            config (Config): The configuration object to add trades to
        """
        for module in self.modules:
            try:
                module.add_trades(config)
            except Exception as e:
                logger.error(f"Error adding trades from {module.__name__}: {e}")

def setup_registry() -> ModuleRegistry:
    """
    Initialize and register all trade modules in the system.
    
    This function creates a new ModuleRegistry and registers all available
    trade modules, organized by game location and mechanics. It includes
    modules for:
    - Core game mechanics
    - London locations
    - Upper River locations
    - Firmament locations
    - Bone Market
    - Rat Market
    - Fate-based activities
    
    Returns:
        ModuleRegistry: A registry containing all registered trade modules
    """
    registry = ModuleRegistry()
    
    # Core modules
    registry.register_module('time_the_healer')
    registry.register_module('social_actions')
    registry.register_module('bazaar')
    registry.register_module('inventory_conversions')
    registry.register_module('rat_market')
    registry.register_module('professional_activities')
    
    # London modules
    london_modules = [
        'london.uncategorized',
        'london.newspaper',
        'london.laboratory',
        'london.hearts_game',
        'london.arbor',
        'london.heists',
        'london.deck_approximation',
        'london.forgotten_quarter'
    ]
    for module in london_modules:
        registry.register_module(module)
    
    # Other location modules
    location_modules = [
        'bone_market.trades',
        'unterzee.khanate',
        'unterzee.wakeful_eye',
        'unterzee.port_cecil',
        'unterzee.gaiders_mourn',
        'parabola.base_camp',
        'parabola.adulterine_castle'
    ]
    for module in location_modules:
        registry.register_module(module)
    
    # Upper River modules
    upper_river_modules = [
        'upper_river.upper_river_exchange',
        'upper_river.uncategorized',
        'upper_river.ealing_gardens',
        'upper_river.jericho',
        'upper_river.evenlode',
        'upper_river.balmoral',
        'upper_river.burrow',
        'upper_river.station_viii',
        'upper_river.moulin',
        'upper_river.hurlers',
        'upper_river.marigold',
        'upper_river.decks',
        'upper_river.tracklayers_city'
    ]
    for module in upper_river_modules:
        registry.register_module(module)
    
    # Firmament modules
    firmament_modules = [
        'firmament.hallows_throat',
        'firmament.midnight_moon',
        'firmament.zenith',
        'firmament.stacks',
        'firmament.risen_burgundy'
    ]
    for module in firmament_modules:
        registry.register_module(module)
    
    # Other modules
    registry.register_module('uncategorized.menace_locations')
    registry.register_module('fate.philosofruits')
    registry.register_module('fate.upwards')
    registry.register_module('fate.whiskerways')
    registry.register_module('posi')
    
    return registry

def main():
    """
    Main entry point for the optimization system.
    
    This function orchestrates the optimization process by:
    1. Setting up the configuration system
    2. Loading and registering all trade modules
    3. Creating and running the optimization
    4. Displaying the results
    
    The function includes error handling to ensure graceful failure and
    informative error messages if something goes wrong.
    """
    try:
        # Setup configuration
        config_manager = ConfigManager()
        config = config_manager.create_optimization_config()
        
        # Setup and initialize trade modules
        registry = setup_registry()
        registry.add_trades(config)
        
        # Create and run optimization
        runner = ModelRunner(
            optimize_input=config_manager.config.optimize_input,
            optimize_output=config_manager.config.optimize_output,
            config=config
        )
        
        # Run optimization and display results
        runner.run_optimization()
        runner.display_summary()
        
    except Exception as e:
        logger.error(f"Error during optimization: {e}")
        raise

if __name__ == "__main__":
    main()