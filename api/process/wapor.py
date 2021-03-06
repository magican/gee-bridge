"""Summary
"""
# import json
import ast
# from jsonpickle import encode, decode
import sys
from StringIO import StringIO

from django.core.management import call_command


class Wapor:
    """docstring for Wapor
    """
    # def __init__(self, *args):
    #     super(Wapor, self).__init__()
    #     for arg in args:
    #         self.arg = arg

    def run(self, *args, **kwargs):
        """Summary

        Args:
            *args: Description
            **kwargs: Description

        Returns:
            TYPE: Description
        """
        # from IPython import embed
        # embed()
        old_stdout = sys.stdout
        # This variable will store everything that is sent to the
        # standard output
        cmd = StringIO()
        sys.stdout = cmd

        # Mock the input data
        MOCK_ARGS = ("wapor",
                     "2015-1-1",
                     "2015-1-30",)

        MOCK_KWARGS = {"map_id": True,
                       "arealstat": ["c", "Benin"],
                       "aggregation": "wp_gb"}

        if not args:
            args = MOCK_ARGS
        if not kwargs:
            kwargs = MOCK_KWARGS

        # Here we can call anything we like, like external modules,
        # and everything that they will send to standard output will be
        # stored on "cmd"
        call_command(*args, **kwargs)

        # Redirect again the std output to screen
        sys.stdout = old_stdout
        lines = cmd.getvalue().split("DEBUG")
        result_maps = {}
        result_stats = {}
        errors = []
        for line in lines:
            print line
            if "RESULT=" in line:
                result_maps = ast.literal_eval(line.split("RESULT=", 1)[1])
            else:
                pass

            if "RESPONSE=" in line:
                result_stats = ast.literal_eval(line.split("RESPONSE=", 1)[1])
            else:
                pass

            if "ERRORS=" in line:
                result_error = str(line.split("ERRORS=", 1)[1])
                errors.append(
                    {"error": "{0}".format(result_error)}
                )
            else:
                pass

        result = {
            "gee_maps": result_maps,
            "gee_stats": result_stats,
            "gee_errors": errors
        }

        return result
