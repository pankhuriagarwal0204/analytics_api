
def main():
    data = [
            {
                "status": "sos",
                "count": 1,
                "day": "2017-01-07",
                "engagement_time": 2000.0
            },
            {
                "status": "neutralized",
                "count": 2,
                "day": "2017-01-02",
                "engagement_time": 4444.0
            },
            {
                "status": "sos",
                "count": 1,
                "day": "2017-01-03",
                "engagement_time": 2000.0
            },
            {
                "status": "neutralized",
                "count": 8,
                "day": "2017-01-01",
                "engagement_time": 16000.0
            },
            {
                "status": "sos",
                "count": 1,
                "day": "2017-01-02",
                "engagement_time": 2000.0
            },
            {
                "status": "sos",
                "count": 1,
                "day": "2017-01-04",
                "engagement_time": 2000.0
            },
            {
                "status": "sos",
                "count": 2,
                "day": "2017-01-01",
                "engagement_time": 4000.0
            },
            {
                "status": "sos",
                "count": 1,
                "day": "2017-01-05",
                "engagement_time": 2000.0
            },
            {
                "status": "sos",
                "count": 1,
                "day": "2017-01-06",
                "engagement_time": 2000.0
            }
        ]
    new = {}
    for i in data:
        if i['day'] not in new :
            new[i['day']] = []
        else:
            pass
        new[i['day']].append('abc')
    print new

if __name__ == '__main__':
    main()