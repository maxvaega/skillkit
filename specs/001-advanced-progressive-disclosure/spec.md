# Feature Specification: Advanced Progressive Disclosure for Agent Skills

**Feature Branch**: `001-advanced-progressive-disclosure`
**Created**: 2025-12-01
**Status**: Draft
**Input**: User description: "Implement a three-level progressive disclosure pattern that minimizes context window usage by loading skill information in stages—from lightweight metadata to full content to supporting files—only as needed by the agent."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Fast Skill Discovery (Priority: P1)

As an agent developer, I need to quickly discover all available skills without loading their full content, so my agent can evaluate options efficiently without exhausting the context window.

**Why this priority**: This is the foundation of progressive disclosure. Without fast metadata loading, the entire system fails to deliver its primary value proposition of memory efficiency.

**Independent Test**: Can be fully tested by initializing a SkillManager with 100 skills and measuring discovery time (<100ms) and memory usage (~2.5MB). Delivers immediate value by enabling agents to see all available skills instantly.

**Acceptance Scenarios**:

1. **Given** 100 skills are available in configured directories, **When** the agent initializes the skill system, **Then** all skill metadata (names, descriptions, allowed tools) loads in under 100ms
2. **Given** skill metadata has been loaded, **When** the agent queries available skills, **Then** no full content has been loaded into memory (memory usage ~2.5MB for 100 skills)
3. **Given** the agent needs to find skills related to "PDF processing", **When** searching by description keywords, **Then** relevant skills are returned instantly without loading their content

---

### User Story 2 - On-Demand Content Loading (Priority: P2)

As an agent, I need to load full skill instructions only when I decide to use a skill, so I can maintain a lean context window while still accessing detailed guidance when needed.

**Why this priority**: Builds on P1 to complete the memory efficiency story. Without this, we'd still have to load all content upfront, defeating the purpose of progressive disclosure.

**Independent Test**: Can be tested by invoking a skill for the first time and verifying that: (1) content loads in <25ms, (2) subsequent invocations use cache (<1ms), and (3) only invoked skills consume additional memory. Delivers value by keeping agent memory usage proportional to actual skill usage.

**Acceptance Scenarios**:

1. **Given** metadata for skill "pdf-extractor" is loaded, **When** the agent invokes the skill for the first time, **Then** full content loads in under 25ms including base directory context
2. **Given** a skill has been invoked once, **When** the agent invokes it again with the same arguments, **Then** cached content is returned in under 1ms
3. **Given** an agent invokes 10 out of 100 available skills, **When** measuring memory usage, **Then** total memory is ~3MB (2.5MB metadata + ~50KB cached content for 10 skills)
4. **Given** a skill contains `$ARGUMENTS` placeholder, **When** the agent invokes it with "file.pdf", **Then** all instances of `$ARGUMENTS` are replaced with "file.pdf" in the processed content
5. **Given** a skill has no `$ARGUMENTS` placeholder, **When** the agent invokes it with arguments "data.csv", **Then** "ARGUMENTS: data.csv" is appended to the processed content

---

### User Story 3 - Secure File Access (Priority: P3)

As an agent, I need to access supporting files (scripts, templates, documentation) referenced in skill instructions, so I can execute complex workflows that require multiple resources while staying within the skill's directory boundaries.

**Why this priority**: Enables advanced skill capabilities but is not essential for basic skill usage. Can be added after core metadata and content loading are working.

**Independent Test**: Can be tested by creating skills with supporting files in subdirectories, invoking the skill to get the base directory path, and then using standard Read/Bash tools to access files. Security validation can be tested independently by attempting directory traversal attacks and verifying they're blocked. Delivers value by enabling sophisticated multi-file skills.

**Acceptance Scenarios**:

1. **Given** a skill has processed content with base directory "/skills/pdf-extractor", **When** the agent needs to read "reference.md", **Then** the agent can construct the path "/skills/pdf-extractor/reference.md" and access it via Read tool
2. **Given** a skill references "scripts/extract.py", **When** the agent resolves the path from base directory, **Then** the full path "/skills/pdf-extractor/scripts/extract.py" is correctly formed
3. **Given** a skill attempts to reference "../sibling-skill/data.csv", **When** the system validates the path, **Then** a security error is raised preventing directory traversal
4. **Given** a skill has subdirectories (scripts/, templates/, docs/), **When** the agent accesses files in these subdirectories, **Then** all paths resolve correctly relative to the skill base directory

---

### Edge Cases

- **What happens when a skill's SKILL.md file is modified after metadata is cached?** System should detect file modification via mtime and invalidate cache entries for that skill.
- **What happens when a skill invocation with empty arguments contains `$ARGUMENTS` placeholders?** All `$ARGUMENTS` instances should be replaced with empty string, potentially leaving grammatically awkward but functionally correct content.
- **What happens when an agent invokes the same skill with different arguments repeatedly?** Each unique (skill_name, arguments) combination gets its own cache entry until LRU eviction occurs at max cache size.
- **What happens when a skill references a file that doesn't exist?** The agent's Read tool will fail with a file not found error—this is expected behavior, as the skill author is responsible for ensuring referenced files exist.
- **What happens when 100+ skills exceed the max cache size (100 entries)?** LRU eviction removes the oldest cached entry to make room for new ones, prioritizing recently-used skills.
- **What happens when skill metadata contains invalid YAML?** Discovery logs a warning and skips that skill, continuing to discover other skills (graceful degradation during discovery).
- **What happens when a skill's name contains special characters or exceeds 64 chars?** Validation raises an error during metadata creation, as skill names must match `^[a-z0-9-]+$` and be max 64 chars.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST load skill metadata (name, description, allowed_tools, version, model, file_path, base_dir, source) without reading full SKILL.md content during discovery
- **FR-002**: System MUST discover 100 skills in under 100ms with memory usage of approximately 2.5MB for metadata only
- **FR-003**: System MUST load full SKILL.md content only when a skill is explicitly invoked by the agent
- **FR-004**: System MUST prepend base directory context line ("Base directory for this skill: {base_dir}") to all processed skill content
- **FR-005**: System MUST support `$ARGUMENTS` placeholder substitution with case-sensitive exact matching, replacing all instances with provided arguments
- **FR-006**: System MUST append "ARGUMENTS: {args}" to content when arguments are provided but no `$ARGUMENTS` placeholder exists
- **FR-007**: System MUST cache processed content using (skill_name, arguments) as cache key to optimize repeated invocations
- **FR-008**: System MUST achieve cache hit rate above 80% for typical usage patterns with cache hits returning content in under 1ms
- **FR-009**: System MUST implement LRU eviction when cache exceeds 100 entries (configurable max_cache_size)
- **FR-010**: System MUST provide cache management methods (clear_cache, get_cache_stats) for monitoring and control
- **FR-011**: System MUST validate all file paths to prevent directory traversal attacks by resolving paths and checking they remain within skill base_dir
- **FR-012**: System MUST reject paths that traverse outside skill base directory with detailed security violation errors
- **FR-013**: System MUST support nested subdirectories (scripts/, templates/, docs/, data/) within skill directories up to 5 levels deep
- **FR-014**: System MUST use yaml.safe_load() for all YAML parsing to prevent code injection vulnerabilities
- **FR-015**: System MUST validate YAML frontmatter structure and detect missing required fields (name, description)
- **FR-016**: System MUST provide both synchronous (discover, invoke_skill) and asynchronous (adiscover, ainvoke_skill) APIs
- **FR-017**: System MUST parse allowed_tools field from metadata but MUST NOT apply any tool restriction logic (deferred to future version)
- **FR-018**: System MUST maintain backward compatibility with all v0.1 and v0.2 APIs while adding new progressive disclosure features
- **FR-019**: System MUST support filtering skills by source (personal, project, plugin), name pattern (regex), and description keywords
- **FR-020**: System MUST provide O(1) lookup time for skills by name using dictionary-based indexing

### Key Entities *(include if feature involves data)*

- **SkillMetadata**: Lightweight metadata containing skill identity (name, description), configuration (allowed_tools, version, model, disable_model_invocation), and file system references (file_path, base_dir, source, plugin_name). Represents Level 1 of progressive disclosure.
- **Skill**: Full skill content containing reference to SkillMetadata, raw markdown content (excluding frontmatter), and processed content (with base directory context and argument substitution). Represents Level 2 of progressive disclosure.
- **ContentCache**: In-memory cache mapping (skill_name, arguments) tuples to processed content strings. Implements LRU eviction and provides hit/miss statistics.
- **SkillPathValidator**: Security component that validates file paths against skill base directory to prevent traversal attacks. Not exposed in public API—used internally by path resolution logic.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Agent systems can discover 100 skills in under 100ms without loading full content, enabling instant skill browsing
- **SC-002**: Memory usage for 100 skills with 10% usage rate is approximately 3MB (2.5MB metadata + 500KB cached content), representing 80% reduction compared to eager loading all content
- **SC-003**: First-time skill invocation completes in under 25ms including file I/O, YAML parsing, base directory injection, and argument substitution
- **SC-004**: Repeated skill invocations with same arguments complete in under 1ms via cache lookup, enabling efficient multi-turn conversations
- **SC-005**: Cache hit rate exceeds 80% for typical agent workflows where skills are invoked multiple times with common arguments
- **SC-006**: All directory traversal attempts are blocked and logged, with zero successful path traversal attacks in security testing
- **SC-007**: Agents can successfully access supporting files (scripts, templates, docs) within skill directories using resolved paths from base directory context
- **SC-008**: Progressive disclosure system maintains backward compatibility with all existing v0.1 and v0.2 functionality, requiring zero changes to existing code
- **SC-009**: System gracefully handles malformed SKILL.md files during discovery (logs warning, continues), but strictly validates during invocation (raises exception)
- **SC-010**: Agent developers can clear cache per-skill or entirely and retrieve cache statistics (size, hits, misses, hit rate) for monitoring

### Assumptions

- Skill files are stored on local filesystem with read access available
- Skill directories follow standard structure with SKILL.md at root and optional subdirectories (scripts/, templates/, docs/, data/)
- YAML frontmatter in SKILL.md files follows documented format with required fields (name, description)
- Typical agent workflows involve discovering many skills but invoking only 10-20% of them
- Skills invoked multiple times tend to use same or similar arguments (enabling cache hits)
- Security validation at path resolution time is sufficient; no additional validation needed at file access time
- LRU cache size of 100 entries is sufficient for typical usage patterns (configurable if needed)
- File modification detection via mtime is acceptable for cache invalidation (no need for hash-based detection)
- Python 3.10+ runtime environment with PyYAML and aiofiles dependencies available

### Dependencies

- Existing v0.2 skillkit implementation (SkillMetadata, Skill dataclasses, SkillDiscovery, SkillParser, SkillManager)
- PyYAML 6.0+ for safe YAML parsing
- aiofiles 23.0+ for async file I/O
- Python 3.10+ standard library (pathlib, functools, dataclasses, typing, asyncio)
- Git branch `001-advanced-progressive-disclosure` for feature development
- Test suite with pytest 7.0+, pytest-asyncio 0.21+ for validation

### Scope Boundaries

**In Scope**:
- Three-level progressive disclosure (metadata → content → files)
- Metadata-only discovery with lazy content loading
- Base directory context injection in processed content
- $ARGUMENTS placeholder substitution with all documented rules
- Content caching with LRU eviction and cache statistics
- Security validation for file path resolution
- Support for nested subdirectories within skills
- Both synchronous and asynchronous APIs
- Backward compatibility with v0.1 and v0.2

**Out of Scope** (deferred to future versions):
- Tool restriction enforcement based on allowed_tools field (v1.1+)
- File modification detection via content hashing (v1.1+)
- Advanced cache eviction strategies beyond LRU (v1.1+)
- Distributed caching or persistent cache storage (v2.0+)
- Real-time skill hot-reloading without cache invalidation (v2.0+)
- Skill versioning and compatibility checking (v2.0+)
- Additional framework integrations beyond LangChain (v1.0+)
- Skill dependency graph and automatic loading of dependencies (v2.0+)
