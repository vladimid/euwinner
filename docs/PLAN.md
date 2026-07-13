 
 

# Plan
## Java to Python Migration for Lottery Wheeling System

### TL;DR
Migrate the `euwin` Spring Boot lottery wheeling system from Java to Python by systematically translating core business logic across seven packages (process, utils, analysis, api, exception, cqrs, validate) while replacing Spring Boot infrastructure with Flask/FastAPI for REST APIs, SQLAlchemy/MongoDB drivers for data persistence, and pytest for testing. This phased approach prioritizes domain logic translation, then infrastructure, avoiding reimplementation of build systems.

### Steps:

1. Define Python architecture & tooling foundation
 - Select web framework (Flask/FastAPI), ORM (SQLAlchemy), and MongoDB driver
 - Create requirements.txt with equivalent dependencies
 - Establish package structure mirroring Java (euwin/analysis, euwin/process, euwin/utils, euwin/api, euwin/exception, euwin/cqrs, euwin/validate)
 - Set up pytest, Mockito-equivalent (pytest-mock), and test fixtures replacing TestContainers
2. Translate core business logic (domain layer first)
 - Migrate exception classes (exception/) → Python custom exceptions
 - Translate CQRS data models (cqrs/) → dataclasses/Pydantic models (DrawEntry, Combination, Draw)
 - Implement validation logic (validate/) → validation functions/decorators
 - Translate analysis algorithms (analysis/) → standalone functions (SingleNumberFrequency, DrawnTogether, AnalysePastDraws*)

3. Migrate CSV processing & data layer
 - Port ExternalResourcesUtils CSV parsing → Python csv module or pandas
 - Create MongoDB connection layer replacing Spring Data MongoDB
 - Create MariaDB abstraction layer replacing Spring Data JPA
 - Implement pagination utilities replacing PageExtractor

4. Translate business/processing services
 - Port process package services → Python service classes (RandomNumbersGenerator, CombinationBuilder, WheelingSystemBuilder)
 - Ensure lottery wheel algorithm logic remains mathematically identical
 - Translate bonus numbers handling logic

5. Build REST API layer
 - Replace four Spring @RestController classes (DataController, AnalysisController, RandomNumbersController, SystemController) with Flask/FastAPI routes
 - Translate request/response mappings, validation, and error handling
 - Implement Swagger/OpenAPI equivalent for API documentation
 - Map endpoint paths and HTTP status codes identically
6. Establish testing strategy & migrate test suite
 - Convert 7 test classes to pytest-based tests
 - Replace TestContainers + MariaDB/MongoDB test containers with pytest fixtures or test database setups
 - Translate Mockito mocks to pytest-mock or unittest.mock
 - Migrate 40+ test data files (CSV, JSON) to fixtures directory
### Further Considerations:
1. Web framework choice: Flask is simpler, FastAPI offers async & automatic OpenAPI docs (closer to Swagger integration). Recommendation: FastAPI for modern async support and schema validation parity with Spring Validation.
2. Data persistence: Decide if MariaDB ↔ MongoDB dual-support is needed post-migration, or consolidate to one. Recommendation: Keep both for now, use SQLAlchemy for relational DB and pymongo for MongoDB.
3. Gradle → setuptools/poetry: Python build tooling differs significantly. Should migration script use setuptools (simpler) or Poetry (more maintainable)? Recommendation: Poetry for dependency management clarity.
4. Bonus numbers complexity: README mentions "accommodate small number of bonus numbers combinations with larger number of main combinations" — verify this wheeling logic is domain-critical before migration. Recommendation: Validate algorithm equivalence in unit tests post-translation.



### Summary (AI):
I've created a high-level migration overview for your euwin project from Java to Python. Here are the 8 key phases:
1. Project Setup - Choose Python framework (FastAPI recommended), configure environment 
2. Domain Models - Convert Java classes/records to Python dataclasses 
3. Business Logic - Migrate analysis, wheeling system builder, and validation packages 
4. API Layer - Convert Spring Controllers to Python web framework routes 
5. Testing - Migrate JUnit tests to pytest 
6. External Resources - Manage CSV/JSON data and database connections 
7. Build & Deployment - Replace Gradle with Python build tools, update Docker
8. Integration & Validation - Test all functionality against existing datasets


The project structure is fairly well-organized with clear separation of concerns (analysis, process, validation, API, utils), which makes it a good candidate for straightforward translation to Python. The migration doesn't require architectural changes—just language and framework equivalents.

