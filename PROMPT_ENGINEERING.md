# Prompt Engineering Documentation

## Overview

This document details the prompt engineering approach used in the AI-Powered Menu Intelligence Widget to generate consistent, high-quality menu descriptions and upsell suggestions.

## Core Prompt Structure

The system uses a carefully crafted prompt that follows best practices for AI interaction:

### 1. Role Definition
```
You are an expert restaurant menu copywriter and sales strategist.
```
- **Purpose**: Establishes expertise and context
- **Benefit**: Ensures AI responds with professional, industry-appropriate language

### 2. Clear Task Definition
```
Your task is to create compelling menu descriptions and upsell suggestions.
```
- **Purpose**: Explicitly states what the AI should do
- **Benefit**: Reduces ambiguity and improves consistency

### 3. Structured Output Requirements

#### Description Requirements (30 words max)
```
1. A BRIEF, ATTRACTIVE DESCRIPTION (maximum 30 words):
   - Highlight key ingredients, flavors, and appeal
   - Use appetizing, descriptive language
   - Focus on what makes this dish special
   - Keep it concise and mouth-watering
```

**Design Rationale**:
- **Word Limit**: 30 words ensures descriptions fit menu constraints
- **Specific Guidelines**: Each bullet point addresses a different aspect
- **Sensory Focus**: Emphasizes taste, texture, and visual appeal

#### Upsell Requirements
```
2. ONE UPSELL SUGGESTION:
   - Suggest a complementary drink, side, or dessert
   - Make it sound irresistible and logical
   - Use persuasive but not pushy language
   - Format as "Pair it with [item]!" or similar
```

**Design Rationale**:
- **Complementary Focus**: Ensures logical pairing
- **Tone Control**: "Persuasive but not pushy" prevents aggressive sales language
- **Format Specification**: Consistent structure for easy integration

### 4. Quality Rules
```
IMPORTANT RULES:
- Description must be exactly 30 words or less
- Use professional, appetizing language
- Avoid generic phrases like "delicious" or "tasty"
- Be specific about flavors, textures, and ingredients
- Make the upsell suggestion relevant and appealing
```

**Design Rationale**:
- **Concrete Constraints**: Specific word limits and banned phrases
- **Quality Standards**: Professional language requirement
- **Specificity Focus**: Encourages detailed, descriptive content

### 5. Structured Response Format
```
Respond in this exact JSON format:
{
    "description": "Your 30-word description here",
    "upsell_suggestion": "Your upsell suggestion here"
}
```

**Design Rationale**:
- **Parseable Output**: JSON format enables easy integration
- **Consistent Structure**: Predictable response format
- **Error Prevention**: Reduces parsing errors in the application

## Prompt Engineering Principles Applied

### 1. Clarity and Specificity
- **Clear Instructions**: Each requirement is explicit and unambiguous
- **Specific Constraints**: Word limits, format requirements, and banned phrases
- **Structured Output**: JSON format ensures consistent parsing

### 2. Context and Role
- **Expert Role**: Positions AI as a professional copywriter
- **Industry Context**: Restaurant-specific language and requirements
- **Purpose Alignment**: Focuses on sales and customer appeal

### 3. Quality Control
- **Validation Rules**: Built-in checks for length and content
- **Language Standards**: Professional, appetizing, specific language
- **Relevance Requirements**: Logical upsell pairings

### 4. Error Prevention
- **Format Specification**: JSON structure prevents parsing errors
- **Length Validation**: Word count limits prevent overflow
- **Sanitization**: Input validation and output cleaning

## Prompt Optimization Techniques

### 1. Iterative Refinement
The prompt was developed through multiple iterations:
- **Version 1**: Basic description generation
- **Version 2**: Added upsell suggestions
- **Version 3**: Implemented word limits and quality rules
- **Version 4**: Added JSON formatting and error prevention

### 2. A/B Testing Approach
Different prompt variations were tested for:
- **Consistency**: Same input produces similar quality output
- **Creativity**: Varied but appropriate descriptions
- **Relevance**: Logical upsell suggestions
- **Length Compliance**: Adherence to word limits

### 3. Edge Case Handling
The prompt addresses common issues:
- **Generic Language**: Explicit ban on "delicious", "tasty"
- **Length Violations**: Clear word count requirements
- **Format Errors**: Structured JSON response
- **Irrelevant Suggestions**: Focus on complementary items

## Model-Specific Considerations

### GPT-3.5 Turbo
- **Faster Response**: Good for real-time applications
- **Cost Effective**: Lower API costs
- **Consistent Quality**: Reliable output for menu descriptions

### GPT-4
- **Enhanced Creativity**: More varied and creative descriptions
- **Better Context Understanding**: Improved comprehension of food items
- **Higher Quality**: More sophisticated language and suggestions

## Integration Considerations

### 1. API Response Handling
```python
# Parse and validate AI response
try:
    parsed_response = json.loads(ai_response)
    # Validate required fields
    if "description" not in parsed_response or "upsell_suggestion" not in parsed_response:
        raise ValueError("Missing required fields")
    # Validate description length
    if len(description.split()) > 30:
        # Truncate to 30 words
        words = description.split()[:30]
        description = " ".join(words)
except json.JSONDecodeError:
    # Fallback to default response
```

### 2. Error Recovery
- **JSON Parsing Errors**: Fallback to default descriptions
- **Length Violations**: Automatic truncation to 30 words
- **API Failures**: Mock responses for demonstration

### 3. Rate Limiting
- **Request Limits**: 10 requests per minute per IP
- **Error Handling**: Graceful degradation under load
- **User Feedback**: Clear error messages for rate limits

## Future Enhancements

### 1. Dynamic Prompting
- **Cuisine-Specific Prompts**: Different prompts for different restaurant types
- **Seasonal Adjustments**: Context-aware seasonal suggestions
- **Price Point Consideration**: Upsell suggestions based on item price

### 2. Multi-Language Support
- **Localized Prompts**: Language-specific prompt variations
- **Cultural Adaptation**: Region-appropriate food descriptions
- **Translation Integration**: Multi-language output support

### 3. Learning and Optimization
- **User Feedback Integration**: Learn from user preferences
- **A/B Testing Framework**: Continuous prompt optimization
- **Performance Analytics**: Track prompt effectiveness

## Best Practices for Prompt Engineering

### 1. Start with Clear Objectives
- Define specific, measurable goals
- Identify target audience and use case
- Establish quality standards and constraints

### 2. Iterate and Test
- Test multiple prompt variations
- Gather feedback from real users
- Measure consistency and quality

### 3. Handle Edge Cases
- Plan for API failures and errors
- Implement fallback mechanisms
- Validate and sanitize all inputs and outputs

### 4. Monitor and Optimize
- Track prompt performance metrics
- Gather user feedback
- Continuously improve based on data

## Conclusion

The prompt engineering approach in this widget demonstrates how careful design can produce consistent, high-quality AI-generated content. By combining clear instructions, structured output, and robust error handling, the system provides reliable menu descriptions and upsell suggestions that enhance the restaurant management experience.

The modular design allows for easy customization and extension, making it suitable for integration into various POS systems and restaurant management platforms.
