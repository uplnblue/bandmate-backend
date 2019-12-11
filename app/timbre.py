import numpy as np

# extract relevant info from segments
def getSegmentInfo(segments):
    seg_info = {
        'timbres': [],
        'segment_start_times': []
    }
    for segment in segments:
        seg_info['timbres'].append(np.array(segment['timbre'][1:6]))
        seg_info['segment_start_times'].append(segment['start'])
    return seg_info

# extra relevant info from sections
def getSectionInfo(sections):
    sect_info = {
        'section_start_times': []
    }
    for section in sections:
        sect_info['section_start_times'].append(section['start'])
    return sect_info

# given the data, produce:
# 1) list of thetas (in radians) between successive timbre vectors
#    averaged over some timescale or section,
#    or if neither kw param is set, then the raw list of thetas

# for now all it can do is "all" precision
# TODO: add for segments, and other precisions
def getThetas(segment_info, section_info, bySection=False, timescale_ms=None):

    def getAngle(v1, v2):
        return np.arccos(v1 @ v2 / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    animation_data = {
        'thetas': [],
        'start_times': []
    }
    # these 2 arrays should always be the same length
    thetas = []
    start_times = []

    for i in range(1, len(segment_info['timbres'])):
        theta = getAngle(np.array(segment_info['timbres'][i]), np.array(segment_info['timbres'][i-1]))
        if not bySection and timescale_ms == None:
            start = segment_info['segment_start_times'][i]
        thetas.append(theta)
        start_times.append(start)

    animation_data['thetas'] = thetas
    animation_data['start_times'] = start_times

    return animation_data
