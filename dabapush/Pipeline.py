"""
Pipelines, you ask? What are pipelines?

---

Well, the easy answer is that pipelines are a sequence of procedures applied to
out data set. A pipeline consist of several steps that depend on the outcome
of each other. Data is passed between the input of one pipeline step and the
output of the preceeding step by the means of python generators.

Thus, a pipeline might be called a higher-order function.
Pipelines must be serializeable.
"""

from yaml import YAMLObject


class Pipeline(YAMLObject):

    