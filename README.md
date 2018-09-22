# 2018-cse-hackathon

# API


Get a list of building names
```
GET /buildings/name
```

```
[
    "Ainsworth",
    ...
]
```

Get a list of building ids
```
GET /buildings/id
```

```
[
    "K17",
    ...
]
```

Get a mapping of building names to ids
```
GET /buildings/mapping
```

```
[
    {"Ainsworth": "J17",
    ...
]
```


Get a list of buildings, and rooms free
```
POST /buildings/free
{
    "epoch_time": 12345
}
```

```
[
    ["J17",
        [
            "201,
            "203",
            ...
        ]
    ],
    ...
]
```


Get a list of room names in a given buildingID
```
GET /rooms/<buildingID>/name
```

```
[
    "Lyre Lab",
    ...
]
```

Get a list of room ids in a given buildingID
```
GET /rooms/<buildingID>/id
```

```
[
    "203",
    ...
]
```


Get a mapping of room names to ids
```
GET /rooms/<buildingID>/mapping
```

```
[
    ["Lyre Lab": "G12"],
    ...
]
```

Get the times occupied for a given buildingID, roomID and time.
The time is a list of integers, from 0 to 47, representing 30 minute intervals from 00:00 to 24:00.
```
POST /rooms
{
    "buildingID": "K17",
    "roomID": "G12",
    "epoch_time": 12345
}
```

```
[
    [
        28,
        29
    ],
    ...
]
```