:::info The query request's are being send as you call the records_paginator
Feel free to break out of the loop of the records_paginator, since the query requests are sent progressively only as you 
iterate over the records_paginator. This means that you call that you cannot calculate the length of records_paginator
in order to know the number of records page to except.
:::