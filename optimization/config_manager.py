"""
Configuration management system for the Fallen London optimization tool.

This module provides functionality for loading, saving, and managing optimization
parameters through a JSON-based configuration system. It handles both the loading
of user-defined configurations and the creation of default configurations when
needed.

The configuration system supports:
- Optimization targets (input/output items)
- Daily action and card limits
- Story and Fate qualities
- Core game constraints
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import json
from pathlib import Path
import logging
from config import Config
from enums import Item

logger = logging.getLogger(__name__)

@dataclass
class OptimizationConfig:
    """
    Configuration dataclass for optimization parameters.
    
    Attributes:
        optimize_input (Item): The resource to optimize for input (e.g., Actions)
        optimize_output (Item): The resource to optimize for output (e.g., Echoes)
        actions_per_day (int): Maximum number of actions available per day
        cards_per_day (int): Maximum number of cards available per day
        story_qualities (Dict[Item, int]): Story-based qualities and their values
        fate_qualities (Dict[Item, int]): Fate-based qualities and their values
        core_constraints (Dict[Item, int]): Core game constraints and their limits
    """
    optimize_input: Item
    optimize_output: Item
    actions_per_day: int
    cards_per_day: int
    story_qualities: Dict[Item, int]
    fate_qualities: Dict[Item, int]
    core_constraints: Dict[Item, int]

class ConfigManager:
    """
    Manages the loading, saving, and creation of optimization configurations.
    
    This class provides a centralized interface for handling configuration data,
    including loading from JSON files, saving to JSON files, and creating
    default configurations when needed.
    
    Attributes:
        config_path (Path): Path to the configuration JSON file
        config (Optional[OptimizationConfig]): The current configuration, if loaded
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the ConfigManager.
        
        Args:
            config_path (str): Path to the configuration JSON file
        """
        self.config_path = Path(config_path)
        self.config: Optional[OptimizationConfig] = None
    
    def load_config(self) -> OptimizationConfig:
        """
        Load configuration from the JSON file.
        
        If the file exists, it will be loaded and parsed. If not, or if there's
        an error loading, a default configuration will be created.
        
        Returns:
            OptimizationConfig: The loaded or default configuration
        """
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    self.config = OptimizationConfig(**data)
                    logger.info(f"Loaded configuration from {self.config_path}")
                    return self.config
            else:
                logger.warning(f"Config file {self.config_path} not found, using defaults")
                return self.create_default_config()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return self.create_default_config()
    
    def save_config(self, config: OptimizationConfig):
        """
        Save the current configuration to the JSON file.
        
        Args:
            config (OptimizationConfig): The configuration to save
        """
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config.__dict__, f, indent=2)
            logger.info(f"Saved configuration to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def create_default_config(self) -> OptimizationConfig:
        """
        Create a default configuration with reasonable starting values.
        
        Returns:
            OptimizationConfig: A new configuration with default values
        """
        return OptimizationConfig(
            optimize_input=Item.Action,
            optimize_output=Item.MourningCandle,
            actions_per_day=120,
            cards_per_day=40,
            story_qualities={
                Item.BagALegend: 4000,
                Item.SetOfCosmogoneSpectacles: 1,
                Item._AllianceWithBigRat: 1,
            },
            fate_qualities={
                Item.AcquaintanceTheClamorousCartographer: 6
            },
            core_constraints={
                Item.Constraint: 1,
                Item.Action: 120 * 7,  # actions_per_day * 7
                Item.GlimEncrustedCarapace: 10,
                Item._RatMarketRotation: 1,
                Item._BoneMarketRotation: 1,
                Item._VisitFromTimeTheHealer: 1,
                Item._CardDraws: 40 * 7,  # cards_per_day * 7
            }
        )
    
    def create_optimization_config(self) -> Config:
        """
        Create a Config object for the optimization engine.
        
        This method combines the loaded configuration with player qualities
        to create a complete Config object ready for optimization.
        
        Returns:
            Config: A complete configuration object for optimization
        """
        if self.config is None:
            self.config = self.load_config()
        
        # Create player with qualities
        from player import Player
        player = Player()
        player.qualities.update(self.config.story_qualities)
        player.qualities.update(self.config.fate_qualities)
        
        # Create and return Config object
        return Config(
            player=player,
            constraint=self.config.core_constraints
        ) 