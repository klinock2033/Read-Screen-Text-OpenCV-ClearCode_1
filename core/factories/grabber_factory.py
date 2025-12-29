from core.contracts.grabber_protocol import GrabberProtocol
from services.mss_grabber import MSSGrabber


def create_grabber(grabber_type: str) -> GrabberProtocol:
    if grabber_type == 'mss':
        return MSSGrabber()

    raise ValueError(f'Invalid grabber type{grabber_type}')