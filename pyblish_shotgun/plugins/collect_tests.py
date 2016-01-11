import pyblish.api
import sys
from .. import lib


class CollectTestObjects(pyblish.api.Collector):
    version = (0, 1, 0)
    order = pyblish.api.Collector.order - 0.1

    def process(self, context):
        context.set_data('testProject', value='test project')


if __name__ == "__main__":
    pass
