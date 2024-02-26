# Redesign of the Data Pipeline

Redesign the DynamoDB Table to support multiple users and multiple types of Logs.

## DynamoDB

Partition Key: UserId:{UserId}
Sort Key: TripName:{TripName}#LogType:{LogType}#Date:{Date}
(Need to think more about the sort key; TripName.)

Single table to support TravelLog, MountainLog, RockLog, IceLog, and SkiLog.

```Typescript
interface AdventureLogItem {
  LogType: string;
  Day: number;
  Date: string;
  StartLoc: string;
  StartLat: number;
  StartLng: number;
  EndLoc: string;
  EndLat: number;
  EndLng: number;
  StartCity: string;
  StartCountry: string;
  StartCountryCode: string;
  StartState: string;
  EndCity: string;
  EndCountry: string;
  EndCountryCode: string;
  EndState: string;
}

interface Sentiment {
  emoji: string;
  label: string;
  score: number;
}

interface TravelLogItem extends AdventureLog {
  TripName: string;
  Day: string;
  WordCount?: number;
  SentenceCount?: number;
  CharacterCount?: number;
  Sentiment?: Array<Sentiment>;
}

interface TravelLogData extends Array<TravelLogItem>{}

interface RockLogItem extends AdventureLog {
  Location: string;
  Type: string;
  Grade: string;
}

interface RockLogData extends Array<RockLogItem>{}

interface IceLogData extends Array<RockLogItem> {}

interface SkiLogItem extends AdventureLog {
  Type: string;
}
```
