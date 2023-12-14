```
   +-------------------+          +---------------------+         +------------------------+
   |   Client          |          |   API Gateway       |         |   Kafka Cluster        |
   |   Applications    |          |                     |         |                        |
   +-------------------+          +---------------------+         |                        |
             |                           |                           |                        |
             v                           v                           |                        |
   +-------------------+          +---------------------+         |                        |
   |   Microservice    |          |   Microservice      |         |   Kafka Topics         |
   |   - Location      |          |   - Person          |         |   - location_created   |
   |   - Person        |          |   - Connection      |         |   - person_created     |
   |   - Connection    |          +---------------------+         +------------------------+
   +-------------------+                    |                         |     |     |
             |                              |                         |     |     |
             |          +-----------------+|                         v     v     v
             +--------->| RPC Server      ||                   +---------------------+
                         | - Person        ||                   | RPC Server          |
                         | - Connection    |+------------------>| - Connection        |
                         +-----------------+|                   +---------------------+
                                             |
                                             v
                                    +---------------------+
                                    |   Microservice      |
                                    |   - Connection      |
                                    |   (continued)       |
                                    +---------------------+

```