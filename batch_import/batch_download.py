#!/usr/bin/env python

DESCRIPTION = \
"""
this script will cycle over a given time-period and download all videos from a given camera that come from
within that time period using the Camio search API (https://api.camio.com/#search)

This script is designed to be used after a batch-import job has been completed and you wish to retreive a
compilation of all of the labels assigned to all of the events that were parsed from the grouping of batch import
video you submitted for the given job.
"""

EXAMPLES = \
"""
Example:

    Here is an example of how to run the script to recover a dictionary of lables for the last job that you 
    submitted
"""

API_NOTES = \
"""
here are some notes on example API calls taken from watching dev-tools in the webapp


{
  "query":
  {
    "date":"2017-05-05T20:06:00.005-0000","sort":"desc","cameras":["sharx"],"labels":[],
	"motion_type":"lmo","object_type":"event","content_type":"image","user":"some_user@camio.com","earliest_date_considered":"2017-05-05T04:24:50.871-0000",
	"latest_date_considered":"2017-05-05T20:01:03.702-0000","text":"sharx some_user@camio.com","remainder":"","zones":[],"colors":[],
	"text_without_date_lowercase":"sharx some_user@camio.com","view_tokens_text_matched":[]
  },
  "result":
  {
    "bucket_type":"event",
	"buckets": [
	{
	  "bucket_id": "hbWlvbG9nZ2VycncLEgVFdmVudCJsZXYtMTA5MDEwNzIyNjg2MjE4NjE0NjIwLTAwRTA0Q0MyN0NDNS4wXzIwMTctMDUtMDVUMjE6MzM6MTYuNDcwOTk4X2Q5MDU4OWIzLTJkNGItNGYyYy1iNTk4LThmZDVkNjJjNzBlNi5qc29uDA",
	  "source": "sharx",
	  "labels": [
	    "_ml_mail",
	    "_ml_departing",
	    "_color_black",
	    "_ml_human",
	    "_color_gray",
	    "_ml_approaching"
	  ],
	  "earliest_date": "2017-05-05T21:32:58.679-0000",
	  "latest_date": "2017-05-05T21:33:06.499-0000",
	  "cover_image_id": "Ijp7ImMiOiJnIiwiayI6ImNvdi0xMDkwMTA3MjI2ODYyMTg2MTQ2MjAtMDBFMDRDQzI3Q0M1LjBfMjAxNy0wNS0wNVQyMTozMzowNC44MDkwNzRfZTJjM2JjOGMtMTlhZi00NGY5LWI0ZjktNTRlY2IyODg4ODFlLmpwZyIsImIiOiJjYW1pb19pbWFnZXMifX0",
	  "max_interest_level": 3,
	  "aspect_ratio": 1.7777778,
	  "images": [
	    {
	      "id": "eyJpZCI6A0Q0MyN0NDNS4wXzIwMTctMDUtMDVUMjE6MzM6MDAuNzA4NDA5Xzg4YmI3MjVjLTk1OGItNDI5Ny1iZmQwLWMyMmE2OTI3M2EzYy5qcGciLCJsIjp7ImMiOiJnIiwiayI6InRoLTEwOTAxMDcyMjY4NjIxODYxNDYyMC0wMEUwNENDMjdDQzUuMF8yMDE3LTA1LTA1VDIxOjMzOjI5LjA2OTI5MV9hZmJhYjZmOC1hMjQ4LTQ1ZjAtOWNiNC02OTg1MjUwYTNmMDIudGh1bWJuYWlscy5qc29uIiwiYiI6ImNhbWlvX2ltYWdlcyJ9fQ",
	      "date_created": "2017-05-05T21:33:00.708-0000",
	      "content_type": "image/jpeg",
	      "source": "sharx",
	      "labels": [
		"_ml_mail",
		"_ml_departing",
		"_color_black",
		"_ml_human",
		"_color_gray",
		"_ml_approaching"
	      ],
	      "interest_level": 0,
	      "interest_score": 0,
	      "access_token": "Y527KlaxCZHpAs_bVWpMRuXcKrdZd_qGTNkkeuCl_cF1OTPQhKeRROXpbOuPiq8rhGnrIOgWOfZW7sBpKqK1jITqZxXe2vGoLVuhPWGSHN5I9sbgMVv4KJ5BdrOZx_wfiynzvCGQwy8BZgwnt0VEtTQiCXHoLNyT45m3ldc0ANJ8u5icyNVALo9ClknRZYoiIJfWiOoVuY2TID-sq6YjGwtAqHkprBv6sUul-9O_QI1l4MNm3JIojXMxLVBIXtHo8MBAle5-HqKKWgRlRm5gRirLL2u4nZDgqrbm2Z1BLkmtJ-MDIOhrttj11iNj9izLZhAA9D9ivhlrDLbgA-iNfedc333wq7aPlv5JWptQ5dGRjzN6891d7Rx1k7NmsWT-dt9fSryJZGgvRE6aEmBJUAzpSKYvkEYGIWDeCmL9Z363vet4RR8jOlAlKS8T-nGEIbmAqwySrkEX33CQKo_j2bCyz25dbHb9Lw"
	    },
	    {
	      "id": "eyJpZCI6IjAwRTA0Q0MyN0NDNS4wXzIwMTctMDUtMDVUMjE6MzM6MDMuNzk1NTE4X2ZhMzUwYzZmLTk4ZTYtNGM3ZS04MjhkLWU0ZTA1OWUwYzhkYS5qcGciLCJsIjp7ImMiOiJnIiwiayI6InRoLTEwOTAxMDcyMjY4NjIxODYxNDYyMC0wMEUwNENDMjdDQzUuMF8yMDE3LTA1LTA1VDIxOjMzOjI5LjA2OTI5MV9hZmJhYjZmOC1hMjQ4LTQ1ZjAtOWNiNC02OTg1MjUwYTNmMDIudGh1bWJuYWlscy5qc29uIiwiYiI6ImNhbWlvX2ltYWdlcyJ9fQ",
	      "date_created": "2017-05-05T21:33:03.795-0000",
	      "content_type": "image/jpeg",
	      "source": "sharx",
	      "labels": [
		"_ml_mail",
		"_ml_departing",
		"_color_black",
		"_ml_human",
		"_color_gray",
		"_ml_approaching"
	      ],
	      "interest_level": 0,
	      "interest_score": 0,
	      "access_token": "AOEU8hgjtjgsV35-Y527KlaxCZHpAs_bVWpMRuXcKrdZd_qGTNkkeuCl_cF1OTPQhKeRROWArjzqdTN-R8qb9jGLI5cMszu2sYSSFEYKNhosntWnxvT52CY_nhKOTO9GbNoZBJy1HPvcdt_VnFcVZFGwhowaD0FWcOTVxEtr94-McX0lLJm3ldc0ANJ8u5icyNVALo9ClknRZYoiIJfWiOoVuY2TID-sq6YjGwtAqHkprBv6sUul-9O_QI1l4MNm3JIojXMxLVBIXtHo8MBAle5-HqKKWgRlRm5gRirLL2u4nZDgqrbm2Z1BLkmtJ-MDIOhrttj11iNj9izLZhAA9D9ivhlrDLbgA-iNfedc333wq7aPlv5JWptQ5dGRjzN6891d7Rx1k7NmsWT-dt9fSryJZGgvRE6aEmBJUAzpSKYvkEYGIWDeCmL9Z363vet4RR8jOlAlKS8T-nGEIbmAqwySrkEX33CQKo_j2bCyz25dbHb9Lw"
	    },
	    {
	      "id": "eyJsIjp7ImMiOiJnIiwiayI6ImNvdi0xMDkwMTA3MjI2ODYyMTg2MTQ2MjAtMDBFMDRDQzI3Q0M1LjBfMjAxNy0wNS0wNVQyMTozMzowNC44MDkwNzRfZTJjM2JjOGMtMTlhZi00NGY5LWI0ZjktNTRlY2IyODg4ODFlLmpwZyIsImIiOiJjYW1pb19pbWFnZXMifX0",
	      "date_created": "2017-05-05T21:33:04.809-0000",
	      "content_type": "image/jpeg",
	      "source": "sharx",
	      "labels": [
		"_ml_mail",
		"_ml_departing",
		"_color_black",
		"_ml_human",
		"_color_gray",
		"_ml_approaching"
	      ],
	      "interest_level": 0,
	      "interest_score": 0,
	      "access_token": "AQCkmgMahb56dfBckAfVXw7q47kASgTjE4Z-SsLrF90IFMnfI6T-Ucc1xQOTPAWdncLuPzdKGHFL85VDlRIR07HdzqZ0eM7Z8ReuE32g3PBTNkAzotdDQnstdazGz4AqFwfHCvcvklloj1yd8x8l_9L60ojl0JkeaMAZtNu82xHw1XrhlaF1LXZqoqjraubx4E1dirme5h3UPURLKh4JxJ2ayIBUfgOp_9Wumi5UJrUyLDA2Lv7qwnLLNUz-iGDx3UlCPCZUFIILvPdsLMB7vsrx_94cVyMIDYJ3nTKh2WDz30Efg2loIdwnIbACvYEPXkQ"
	    },
	    {
	      "id": "eyJpZCI6IjAwRTA0Q0MyN0NDNS4wXzIwMTctMDUtMDVUMjE6MzM6MDUuNDMxODQxXzEzYjdhNjU5LTEyMWMtNDAyYy04ODk3LTlmMWVkYWVkYzM5Mi5qcGciLCJsIjp7ImMiOiJnIiwiayI6InRoLTEwOTAxMDcyMjY4NjIxODYxNDYyMC0wMEUwNENDMjdDQzUuMF8yMDE3LTA1LTA1VDIxOjMzOjI5LjA2OTI5MV9hZmJhYjZmOC1hMjQ4LTQ1ZjAtOWNiNC02OTg1MjUwYTNmMDIudGh1bWJuYWlscy5qc29uIiwiYiI6ImNhbWlvX2ltYWdlcyJ9fQ",
	      "date_created": "2017-05-05T21:33:05.431-0000",
	      "content_type": "image/jpeg",
	      "source": "sharx",
	      "labels": [
		"_ml_mail",
		"_ml_departing",
		"_color_black",
		"_ml_human",
		"_color_gray",
		"_ml_approaching"
	      ],
	      "interest_level": 0,
	      "interest_score": 0,
	      "access_token": "AOEU8hgjtjgsV35-Y527KlaxCZHpAs_bVWpMRuXcKrdZd_qGTNkkeuCl_cF1OTPQhKeRROWMRTnFFffpv_fz2NKxQUGeDoySFALvkAbgxIlEGZn0TYZkrz-_TO9iiDSPWF276EWgDgVIR9gbhdSMMeVoxL5FAGSd_RvgPnVSc64AZmCL3Jm3ldc0ANJ8u5icyNVALo9ClknRZYoiIJfWiOoVuY2TID-sq6YjGwtAqHkprBv6sUul-9O_QI1l4MNm3JIojXMxLVBIXtHo8MBAle5-HqKKWgRlRm5gRirLL2u4nZDgqrbm2Z1BLkmtJ-MDIOhrttj11iNj9izLZhAA9D9ivhlrDLbgA-iNfedc333wq7aPlv5JWptQ5dGRjzN6891d7Rx1k7NmsWT-dt9fSryJZGgvRE6aEmBJUAzpSKYvkEYGIWDeCmL9Z363vet4RR8jOlAlKS8T-nGEIbmAqwySrkEX33CQKo_j2bCyz25dbHb9Lw"
	    },
	    {
	      "id": "eyJpZCI6IjAwRTA0Q0MyN0NDNS4wXzIwMTctMDUtMDVUMjE6MzM6MDYuNDk5NDQxXzRmODYzN2RiLTk1MGQtNGQ3YS05NDlhLTYxZjc1YzNiNDBmMi5qcGciLCJsIjp7ImMiOiJnIiwiayI6InRoLTEwOTAxMDcyMjY4NjIxODYxNDYyMC0wMEUwNENDMjdDQzUuMF8yMDE3LTA1LTA1VDIxOjMzOjI5LjA2OTI5MV9hZmJhYjZmOC1hMjQ4LTQ1ZjAtOWNiNC02OTg1MjUwYTNmMDIudGh1bWJuYWlscy5qc29uIiwiYiI6ImNhbWlvX2ltYWdlcyJ9fQ",
	      "date_created": "2017-05-05T21:33:06.499-0000",
	      "content_type": "image/jpeg",
	      "source": "sharx",
	    "labels": [
		"_ml_mail",
		"_ml_departing",
		"_color_black",
		"_ml_human",
		"_color_gray",
		"_ml_approaching"
	      ],
	      "interest_level": 0,
	      "interest_score": 0,
	      "access_token": "AOEU8hgjtjgsV35-Y527KlaxCZHpAs_bVWpMRuXcKrdZd_qGTNkkeuCl_cF1OTPQhKeRROXNFavajVtKzv2M8TMJH7crnDPf5e1xThxa_d9bRzGtlVkuK656GcnyvlVlvwAJllNmCONRRZKGdw0Iyikr_9LRpNPkb74Fyy6DukNk5WCDMJm3ldc0ANJ8u5icyNVALo9ClknRZYoiIJfWiOoVuY2TID-sq6YjGwtAqHkprBv6sUul-9O_QI1l4MNm3JIojXMxLVBIXtHo8MBAle5-HqKKWgRlRm5gRirLL2u4nZDgqrbm2Z1BLkmtJ-MDIOhrttj11iNj9izLZhAA9D9ivhlrDLbgA-iNfedc333wq7aPlv5JWptQ5dGRjzN6891d7Rx1k7NmsWT-dt9fSryJZGgvRE6aEmBJUAzpSKYvkEYGIWDeCmL9Z363vet4RR8jOlAlKS8T-nGEIbmAqwySrkEX33CQKo_j2bCyz25dbHb9Lw"
	    }
	  ],
	  "videos": [
	    {
	      "id": "ljskdlkjjoiQVFDellvMzZLZ2NpaW5fenRYNFNjQVlrazNHNUZQengzXzc5bGx4a0s4UlVRN1pPRW5yeEREdjBNN3VYN2hSNGI4TklNbGFUWW9Jb0tURTdPTWxoUVduUy1Ua3ZGTmdnRHBLeHNjYnN4d2FTLWpNS2I3S1g0bVJ2azFYQmhacTJOODJCYnoyVmpwV2NCdlRPVUN0RnlEQnNiYTVLWlNfdDhXYXdjRndXejhyOG1ncG51WTY3c2VPTTQwRnpiQ1hNWGxrIiwibCI6eyJjIjoiZyIsImsiOiJtdi0xMDkwMTA3MjI2ODYyMTg2MTQ2MjAtMDBFMDRDQzI3Q0M1LjBfMjAxNy0wNS0wNVQyMTozMjo1My44Mjg1NjVfNzI5NWJmODQtOGY2Ni00M2JiLTgxYjYtMTkwMjdjOGM4YWMwLm1wNCIsImIiOiJjYW1pbyJ9fQ",
	      "date_created": "2017-05-05T21:32:53.828-0000",
	      "content_type": "video/mp4",
	      "source": "sharx",
	      "labels": [
		"_ml_mail",
		"_ml_departing",
		"_color_black",
		"_ml_human",
		"_color_gray",
		"_ml_approaching"
	      ],
	      "video_length": 11.29,
	      "interest_level": 0,
	      "interest_score": 0,
	      "movie": {
		"server_id": "mv-109010722686218614620-00E04CC27CC5.0_2017-05-05T21:32:53.828565_7295bf84-8f66-43bb-81b6-19027c8c8ac0.mp4",
		"content_type": "video/mp4",
		"duration_sec": 11.29,
		"timestamp": {
		  "meta_class": "datetime.datetime",
		  "date": "2017-05-05T21:32:53.828565"
		},
		"playback_speed_ratio": 1,
		"format_info": {
		  "codec_name": "h264",
		  "profile": "Baseline"
		}
	      }
	    },
	    {
	      "id": "ljskdlkjjoiQVFDellvMzZLZ2NpaW5fenRYNFNjQVlrazNHNUZQengzXzc5bGx4a0s4UlVRN1pPRW5yeEREdjBNN3VYN2hSNGI4UEdDRS10MmctZHJfQk5TVkg4M2h6ZTdaM3VvWWxXNjhqVDRjVER2ZXRpbExMeHRFNlZvQTlVcDM4aTEzSldqTGhIUkI2c3F6ejEtSjVic1FvVGo1RzFiYTVLWlNfdDhXYXdjRndXejhyOG1ncG51WTY3c2VPTTQwRnpiQ1hNWGxrIiwibCI6eyJjIjoiZyIsImsiOiJtdi0xMDkwMTA3MjI2ODYyMTg2MTQ2MjAtMDBFMDRDQzI3Q0M1LjBfMjAxNy0wNS0wNVQyMTozMzowNC4yNzUyNzRfNjFiMmQwNDctOWY1OC00NTUyLWI0Y2EtNzdhODYxZjVmZDJjLm1wNCIsImIiOiJjYW1pbyJ9fQ",
	      "date_created": "2017-05-05T21:33:04.275-0000",
	      "content_type": "video/mp4",
	      "source": "sharx",
	      "labels": [
		"_ml_mail",
		"_ml_departing",
		"_color_black",
		"_ml_human",
		"_color_gray",
		"_ml_approaching"
	      ],
	      "video_length": 10.676,
	      "interest_level": 0,
	      "interest_score": 0,
	      "movie": {
		"server_id": "mv-109010722686218614620-00E04CC27CC5.0_2017-05-05T21:33:04.275274_61b2d047-9f58-4552-b4ca-77a861f5fd2c.mp4",
		"content_type": "video/mp4",
		"duration_sec": 10.676,
		"timestamp": {
		  "meta_class": "datetime.datetime",
		  "date": "2017-05-05T21:33:04.275274"
		},
		"playback_speed_ratio": 1,
		"format_info": {
		  "codec_name": "h264",
		  "profile": "Baseline"
		}
	      }
	    }
	  ],
	  "color": "#dadada",
	  "count": 6
	}
	"more_buckets": "listed_below ...",
    } # end buckets	
} # end entire payload


"""

import os
import sys
import argparse
import json
import requests
import textwrap



class BatchDownloader(object):

    def __init__(self):
        # TODO - change the URLs to test.camio.com instead of test.camio.com after deployed to prod
        self.CAMIO_JOBS_URL = "https://test.camio.com/api/jobs"
        self.CAMIO_PARAMS = {}
        self.CAMIO_OAUTH_TOKEN_ENVVAR = "CAMIO_OAUTH_TOKEN"

        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description = textwrap.dedent(DESCRIPTION), epilog=EXAMPLES
        )
        # positional args
        self.parser.add_argument('job_id', type=str, help='the ID of the job that you wish to download the labels for')
        # optional arguments
        self.parser.add_argument('-a', '--access_token', type=str, help='your Camio OAuth token (if not given we check the CAMIO_OAUTH_TOKEN envvar)')

    def get_access_token(self):
        if not self.CAMIO_PARAMS.get('access_token'):
            token = os.environ.get(self.CAMIO_OAUTH_TOKEN_ENVVAR)
            if not token:
                fail("unable to find Camio OAuth token in either hook-params json or CAMIO_OAUTH_TOKEN envvar. \
                     Please set or submit this token")
            self.CAMIO_PARAMS['access_token'] = token
        return self.CAMIO_PARAMS['access_token']

    def parse_argv_or_exit(self):
        self.args = parser.parse_args()
        if self.args.access_token:
            self.CAMIO_PARAMS['access_token'] = self.args.access_token
        return self.args
            

    def get_results_for_epoch(self, start_time, end_time, camera_name):
        """ 
        use the Camio search API to return all of the search results for the given camera between the two unix-style timestamps
        these search results can then be parsed and the meta-data about the labels added to each event can be extracted and assembled
        into a dictionary of some sorts to be returned to the user
        """
        pass


def main():
    args = parse_argv_or_exit()

if __name__ == '__main__':
    main()

