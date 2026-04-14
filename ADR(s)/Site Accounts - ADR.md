# Core Functionality

## 31/03/2026 Revision:

### Status:
Approved

### Context
To prevent service abuse or requests from being misattributed, mechanisms for identifying users and granting them relevant access must be implemented.

### Alternative Solutions Considered
1. Account unique to application
  - Pros
    - No reliance on systems established externally of the application
  - Cons
    - Moderate data security is required for account protection
2. No accounts 
  - Pros
    - No reliance on systems established externally of the application
    - No account protection required
  - Cons
    - Hard to validate users 
    - Significant risk of abuse
    - Significant risk of ticket misattribution 

### Solution Decided Upon:
Linked to the Australian Government MyGov account – As the application will be closely tied to the region's civil services, it can be assumed that this application will be proposed for government use. Meaning, it can tie into the network of government sites that require MyGov accounts. Which individuals living rurally are increasingly making greater use of. Therefore, it is easier to validate users and properly attribute tickets. As well as communicate via means users may have connected to their MyGov account.

### Consequences:
Data security is still an issue, especially as it relates to a government account and whatever the user may have tied to it. It also requires implementing a login system when made publicly accessible. 

### Code Reference:
...
