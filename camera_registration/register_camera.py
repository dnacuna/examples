#!/usr/bin/env python

DESCRIPTION = \
"""
this script allows you to register a camera source with the Camio service through 
the /api/devices/registered endpoint. Camera registration is normally done automatically 
by a Camio Box that scans the local network and automatically detects and registers the cameras
that it finds. This script allows you to register a camera that a Camio Box doesn't know how to recognize.

This script allows you to connect your cameras/nvrs/dvrs with the Camio service,
they can use this script to register their device with the correct RTSP connection information. Once registered, 
the camera/dvr/nvr will show up as an entry on your https://www.camio.com/boxes page, where you can choose to connect
it to a Camio Box and have the video stream processed.

To connect a camera to your Camio account, you must specify the Camio Box device that you will be connecting the camera 
to our servers through. You do this by providing the device ID of the Camio Box to this script. Currently, the easiest way
to get the device ID is by going to your https://www.camio.com/boxes page and getting the device ID out of the URL.
(the URL will look like: https://www.camio.com/boxes?device_id=AABBCCDDEFFAABBDDEEFFCC, grab the AABBCCDDEFFAABBDDEEFFCC part)

*NOTE* - Camio only supports H264 encoded video streams, mjpeg, etc. will not work.

Camio uses mustache-style placeholders in the RTSP URLs for the following values:
    username
    password
    ip_address
    port
    stream
    channel

You can place these as {{placeholder}} anywhere inside of the RTSP URL, and we will fill in the appropriate values before attempting to
connect to the given device.
"""

EXAMPLES = \
"""
Examples:

To register a camera with:
name:        my_new_camera
make:        Hikvision
model:       DCS-2302-I
username:    admin
password:    admin
port:        8080
ip address:  192.168.1.18
RTSP URL:    rtsp://{{username}}:{{password}}@{{ip_address}}:{{port}}/live/{{stream}}.h264
camera-ID:   AABBCCDDEEDD.0
MAC address: AABBCCDDEEDD

you would do the following:

python register_camera.py -v -u admin -p admin -s 1 -i 192.168.1.18 -p 8080 \\
        --make Hikvision --model DCS-2302-I \\
        rtsp://{{username}}:{{password}}@{{ip_address}}:{{port}} \\
        /live/{{stream}}.h264 AABBCCDDEEDD AABBCCDDEEDD.0 my_new_camera \\
        $CAMIO_ACCOUNT_AUTH_TOKEN $CAMIOBOX_DEVICE_ID
"""

import argparse
import sys
import os
import json
import textwrap
import requests
import logging

CAMIO_SERVER_URL = "https://www.camio.com"
CAMIO_TEST_SERVER_URL = "https://test.camio.com"

REGISTER_CAMERA_ENDPOINT = "/api/cameras/discovered"
DEBUG_OUTPUT = False

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def parse_cmd_line_or_exit():
    global DEBUG_OUTPUT
    global CAMIO_SERVER_URL
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description = textwrap.dedent(DESCRIPTION), epilog=EXAMPLES
    )

    # optional arguments / flags
    parser.add_argument('-u', '--username', type=str, help='the username used to access the RTSP stream')
    parser.add_argument('-p', '--password', type=str, help='the password used to access the RTSP stream')
    parser.add_argument('-s', '--stream', type=str, help='the selected stream to use in the RTSP URL')
    parser.add_argument('-c', '--channel', type=str, help='the selected stream to use in the RTSP URL')
    parser.add_argument('-P', '--port', type=int, help='the port that the RTSP stream is accessed through', default=554)
    parser.add_argument('-i', '--ip_address', type=str, help='The IP address of the camera (local or external)')
    parser.add_argument('--maker', type=str, help='the make (manufacturer name) of the camera')
    parser.add_argument('--model', type=str, help='the model of the camera')
    parser.add_argument('--test', action='store_true', help='use the Camio testing servers instead of production')
    parser.add_argument('-v', '--verbose', action='store_true', help='print extra information to stdout for debugging purposes')
    parser.add_argument('--img_x_size_cover', type=int, help='width (pixels) of the cover image')
    parser.add_argument('--img_y_size_cover', type=int, help='height (pixels) of the cover image')
    parser.add_argument('--img_x_size', type=int, help='width (pixels) of the other thumbnails')
    parser.add_argument('--img_y_size', type=int, help='height (pixels) of the other thumbnails')

    # positional arguments
    parser.add_argument('rtsp_server', type=str, 
        help='the RTSP URL that identifies the video server, with placeholder (e.g. rtsp://{{username}}:{{password}}@{{ip_address}})'
    )
    parser.add_argument('rtsp_path', type=str, 
        help='the path that is appended to the rtsp_server value to construct the final RTSP URL, with placeholders (e.g. /live/{{stream}}.h264)'
    )
    parser.add_argument('mac_address', type=str, help='the MAC address of the device being connected to')
    parser.add_argument('local_camera_id', type=str, help='some string representing an ID for your camera. Must be unique per account')
    parser.add_argument('camera_name', type=str, help='some user-friendly name for your camera')
    parser.add_argument('auth_token', type=str, help='your Camio OAuth token (see https://www.camio.com/settings/integrations/#api)')
    parser.add_argument('device_id', type=str, help='the device ID of the Camio Box you wish to connect this camera to')
    args = parser.parse_args()
    if args.verbose: logging.getLogger().setLevel(logging.DEBUG)
    if args.test: CAMIO_SERVER_URL = CAMIO_TEST_SERVER_URL
    return args

def generate_actual_values(arg_dict):
    actual_values=dict()
    for item in [x for x in ['username', 'password', 'port'] if arg_dict.get(x)]:
        actual_values[item] = dict(options=[{'value': arg_dict.get(item)}])
    for item in [x for x in ['stream', 'channel'] if arg_dict.get(x)]:
        actual_values[item] = dict( 
            options = [ {'name': "%s %s" % (item, arg_dict.get(item)), 'value': arg_dict.get(item)}]
        )
    if arg_dict.get('img_y_size_cover') or arg_dict.get('img_y_size'):
        arg_dict['img_y_size_extraction'] = max(
            arg_dict.get('img_y_size_cover', 1), arg_dict.get('img_y_size', 1)
        )    
    for item in ['img_%s_size%s' % (x,y) for x in ['x', 'y'] for y in ['', '_cover', '_extraction']]:
        logging.debug("checking for item: %s, args.%s = %r", item, item, arg_dict.get(item))
        if not arg_dict.get(item): continue 
        actual_values[item] = dict(options=[{'value': arg_dict.get(item)}])
    logging.debug("calculated actual values:\n%r", json.dumps(actual_values))
    return actual_values
    
def generate_payload(args):
    arg_dict = args.__dict__
    actual_values = generate_actual_values(arg_dict)
    payload = dict(
        local_camera_id=args.local_camera_id,
        name=args.camera_name,
        mac_address=args.mac_address,
        maker=arg_dict.get('maker', ''), 
        model=arg_dict.get('model', ''), 
        ip_address=arg_dict.get('ip_address', ''), # ip address might not always be specified separately 
        rtsp_server=args.rtsp_server,
        rtsp_path=args.rtsp_path,
        actual_values=actual_values,
        default_values=actual_values,
        device_id_discovering=args.device_id
    )
    payload = { args.local_camera_id: payload }
    logging.debug("JSON payload to Camio Servers:\n %s" % json.dumps(payload))
    return payload

def generate_headers(args):
    headers = {"Authorization": "token %s" % args.auth_token}
    logging.debug("Generated Headers:\n %s" % headers)
    return headers

def post_payload(payload, headers):
    url = CAMIO_SERVER_URL + REGISTER_CAMERA_ENDPOINT
    ret = requests.post(url, headers=headers, json=payload)
    logging.debug("return from POST to /api/cameras/discovered:\n %s" % vars(ret))
    return ret.status_code in (200, 204)

def main():
    args = parse_cmd_line_or_exit()
    logging.debug("Parsed command line arguments:\n %s" % args.__dict__)
    post_values = generate_payload(args)
    headers = generate_headers(args)
    if not post_payload(post_values, headers):
        logging.error("error registering camera (name: %s, ID: %s) with Camio servers",
                      args.camera_name, args.local_camera_id)
        sys.exit(1)
    logging.info("successfully registered camera (name: %s, ID: %s) with Camio servers",
                 args.camera_name, args.local_camera_id)
    sys.exit(0)


if __name__ == '__main__':
    main()
