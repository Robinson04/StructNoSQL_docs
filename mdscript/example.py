from mdscript.config import MDScriptConfig
from mdscript.runner import Runner
from mdscript.transformers import FileImportTransformer, FileTemplateTransformer, StructNoSQLSampleTransformer

Runner(
    MDScriptConfig(
        transformers={
            'sampler': StructNoSQLSampleTransformer,
            'file': FileImportTransformer,
            'template': FileTemplateTransformer
        }
    ),
    base_dirpath='F:/Inoft/StructNoSQL/docs/docs'
).start()
