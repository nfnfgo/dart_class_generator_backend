'''The tools function for this generator program'''


def intend(intend_level: int):
    '''Return some spaces based on the '''
    intend_str: str = ''
    # add space
    for i in range(intend_level):
        intend_str += '  '
    return intend_str


def changeline_intend(intend_level: int):
    '''Return a linebreak and some intend based on the intend level'''
    return '\n' + intend(intend_level)
