---
id: ActiveSelf
slug: /api/ActiveSelf
---

**A special object that allow to reference a model from inside itself, which allows recursive nesting of models.**

```python
from StructNoSQL import BaseField, ActiveSelf
from typing import Dict

childParameters = BaseField(field_type=Dict[str, ActiveSelf])
```

For detailed explanations on using recursive nesting, see : [Recursive nesting](../basics/recursive_nesting)
