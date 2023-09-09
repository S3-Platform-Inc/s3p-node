```python
class <parser name >:

    def __init__(self, < driver selenium >, *args, **kwargs): ...

    def content(self) -> list[SPP_document]: ...

    def _parser(self, *args, **kwargs): ...

    < other
    methods >
```

```mysql
# This spp_plugin processes File source
# Link: https://www.pcisecuritystandards.org
# Author:
#	Roman Lupashko
#	NSPK DI

SOURCE <source name>

PARSER <parser filename>

SETENV LogMode debug

BUS_ADD s_download PARSER/PCI/temp_download

INIT driver WebDriver
START
<class parser name> content

ADD FilterOnlyNewDocumentWithDB
ADD DownloadDocumentsThroughSeleniumTemp
ADD ExtractTextFromFile
ADD UploadDocumentToDB

```