from mdscript import MDScriptConfig, Runner
from mdscript.transformers import FileImportTransformer, StructNoSQLSampleTransformer

Runner(
    MDScriptConfig(
        transformers={
            'sampler': StructNoSQLSampleTransformer,
            'file': FileImportTransformer
        }
    ),
    base_dirpath='F:/Inoft/StructNoSQL/docs/docs'
).start()
