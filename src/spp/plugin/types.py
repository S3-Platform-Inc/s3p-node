"""
This module defines the plugin types used by the node working

- SOURCE    -это плагины, которые занимаются обработкой источников (например, парсеры)
- ML        -это плагины, которые определяют и запускают модели
- PIPELINE  -это плагины только с постобработкой
"""

SOURCE = 'SOURCE'
ML = 'ML'
PIPELINE = 'PIPELINE'
