import json
import traceback

import cherrypy

import tangelo

class TangeloStream(object):
    def __init__(self):
        self.streams = {}

    @cherrypy.expose
    def default(self, key, action="next"):
        if action != "show":
            # Check for key parameter.
            if key is None:
                raise cherrypy.HTTPError("400 Required Query Parameter Missing", "The streaming API requires a 'key' query parameter")

            # Check that the key actually exists.
            if key not in self.streams:
                raise cherrypy.HTTPError("404 Key Not Found", "The key '%s' does not reference any existing stream" % (key))

        # Construct an empty response object.
        result = {}

        # Perform the requested action.
        actions = ["next", "delete", "show"]
        if action == "next":
            # Grab the stream in preparation for running it.
            stream = self.streams[key]

            # Attempt to run the stream via its next() method - if this yields a
            # result, then continue; if the next() method raises StopIteration,
            # then there are no more results to retrieve; if any other exception
            # is raised, this is treated as an error.
            try:
                result["stream_finished"] = False
                result["result"] = stream.next()
            except StopIteration:
                result["stream_finished"] = True
                del self.streams[key]
            except:
                del self.streams[key]
                raise cherrypy.HTTPError("501 Error in Python Service", "Caught exception while executing stream service keyed by %s:<br><pre>%s</pre>" % (key, traceback.format_exc()))

        elif action == "delete":
            del self.streams[key]
            result["result"] = "OK"
        elif action == "show":
            raise cherrypy.HTTPError("501 Unimplemented", "The 'show' action in the Tangelo streaming API has not yet been implemented")
        else:
            raise cherrypy.HTTPError("400 Bad Query Parameter", "The 'action' parameter must be one of: %s" % (", ".join(actions)))

        try:
            result = json.dumps(result)
        except TypeError:
            raise cherrypy.HTTPError("501 Bad Response from Python Service", "The stream keyed by %s returned a non JSON-seriazable result: %s" % (key, result["result"]))

        return result

    def add(self, stream):
        # Generate a key corresponding to this object.
        key = tangelo.util.generate_key(self.streams)

        # Log the object in the streaming table.
        self.streams[key] = stream

        # Create an object describing the logging of the generator object.
        result = {"stream_key": key}

        # Serialize it to JSON.
        return json.dumps(result)
