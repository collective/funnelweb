
import mr.migrator.runner

def runner(args={}, pipeline=None):
    if pipeline is None:
        pipeline = "funnelweb.remote"
    mr.migrator.runner.runner(args, pipeline)
