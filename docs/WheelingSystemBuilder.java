
package com.vld.euwin.process;
import tools.jackson.databind.JsonNode;
import tools.jackson.databind.ObjectMapper;
import com.vld.euwin.exception.InvalidSchemaException;
import com.vld.euwin.exception.NullParameterException;
import com.vld.euwin.exception.OutOfRangeException;
import com.vld.euwin.utils.CommonConstants;
import com.vld.euwin.validate.CombinationValidation;
import com.vld.euwin.validate.SchemaValidation;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;


@Service
public class WheelingSystemBuilder {

    private static final Logger LOGGER = LoggerFactory.getLogger(WheelingSystemBuilder.class);

    public static final String RETURN_JSON = "Numbers returned:\n %s";
    public static final String BONUS_SYSTEM_SIZE = "bonusSystemSize";
    public static final String MAIN_GAME_POOL = "mainGamePool";
    public static final String BONUS_POOL = "bonusPool";
    public static final String MAIN_NUMBERS_COMBINATION = "mainNumbersCombination";
    public static final String BONUS_NUMBERS = "bonusNumbers";
    public static final String MAIN_GAME_SIZE = "mainGameSize";
    public static final String MAIN_SYSTEM_SIZE = "mainSystemSize";

    @Autowired
    private CombinationBuilder combinationBuilder;

    @Autowired
    private RandomNumbersGenerator randomNumbersGenerator;

    @Autowired
    private CombinationValidation combinationValidation;

    @Autowired
    private SchemaValidation schemaValidation;

    /**
     * Build a shorthand (wheeling) system of lottery lines (combinations)
     *
     * @param requestParameters The numbers and parameters needed for building of a shorthand system.
     * @return JsonNode A shorthand system built from the given parameters.
     */
    public JsonNode buildWheelingSystem(JsonNode requestParameters) {
        LOGGER.info("WheelingSystemBuilder.buildWheelingSystem");
        if (null == requestParameters) {
            LOGGER.error(CommonConstants.EMPTY_JSON_ERROR);
            throw new NullParameterException(CommonConstants.EMPTY_JSON_ERROR);
        }

        if (LOGGER.isDebugEnabled()) {
            LOGGER.debug(requestParameters.asText());
        }
        // get JSON object
        ObjectMapper mapper = new ObjectMapper();
        Map<String, Object> parameters = mapper.convertValue(requestParameters, Map.class);

        if (!schemaValidation.validSchema(parameters.keySet())){
            throw new InvalidSchemaException("Request is missing parameters or contains wrong ones");
        }

        // derive variables/params from it
        Integer mainGamePool = (Integer) parameters.get(MAIN_GAME_POOL);

        List<Integer> mainNumbersCombination =
                ((ArrayList<Integer>) parameters.get(MAIN_NUMBERS_COMBINATION))
                        .stream().distinct().sorted().collect(Collectors.toList());

        String invalidRange = combinationValidation.invalidRange(mainNumbersCombination, mainGamePool);
        if(!invalidRange.isEmpty()){
            throw new OutOfRangeException(invalidRange);
        }

        Integer bonusPool = (Integer) parameters.get(BONUS_POOL);

        List<Integer> bonusNumbers = null;
        Optional<List<Integer>> bonusNumbersOpt;
        bonusNumbersOpt = Optional.ofNullable((List<Integer>) parameters.get(BONUS_NUMBERS));
        if (bonusNumbersOpt.isPresent()) {
            bonusNumbers = bonusNumbersOpt.get().stream().distinct().sorted().collect(Collectors.toList());
            invalidRange = combinationValidation.invalidRange(bonusNumbers, bonusPool);
            if(!invalidRange.isEmpty()){
                throw new OutOfRangeException(invalidRange);
            }
        }


        Integer mainGameSize = (Integer) parameters.get(MAIN_GAME_SIZE);
        Integer mainSystemSize = (Integer) parameters.get(MAIN_SYSTEM_SIZE);

        Optional<Integer> bonusSizeOpt;
        bonusSizeOpt = Optional.ofNullable((Integer) parameters.get(BONUS_SYSTEM_SIZE));
        Integer bonusSize = null;
        if (bonusSizeOpt.isPresent()) {
            bonusSize = bonusSizeOpt.get();
        }

        Integer bonusSystemSize = (Integer) parameters.get(BONUS_SYSTEM_SIZE);

        JsonNode wheelingSystem = combinationBuilder
                .createWheelingCombinations(mainNumbersCombination, bonusNumbers,
                        mainGameSize, mainSystemSize, bonusSize, bonusSystemSize);

        if (LOGGER.isDebugEnabled()) {
            LOGGER.debug(String.format(RETURN_JSON, wheelingSystem.asText()));
        }
        return wheelingSystem;
    }


    /**
     * Generate a shorthand system of combinations of random numbers
     *
     * @param requestData The parameters needed to build a  shorthand system of random numbers.
     * @return
     */
    public JsonNode buildRandomWheelingSystem(JsonNode requestData) {
        LOGGER.info("WheelingSystemBuilder.buildRandomWheelingSystem");
        if (null == requestData) {
            LOGGER.error(CommonConstants.EMPTY_JSON_ERROR);
            throw new NullParameterException(CommonConstants.EMPTY_JSON_ERROR);
        }

        if (LOGGER.isDebugEnabled()) {
            LOGGER.debug(requestData.asText());
        }
        // get JSON object
        ObjectMapper mapper = new ObjectMapper();
        Map<String, Object> parameters = mapper.convertValue(requestData, Map.class);

        Integer mainGamePoolSize = (Integer) parameters.get("mainGamePoolSize");
        Integer fullSystemSize = (Integer) parameters.get("fullSystemSize");
        List<Integer> mainNumbersCombination = randomNumbersGenerator.getRandomCombination(mainGamePoolSize, fullSystemSize);

        Integer bonusGamePoolSize = (Integer) parameters.get("bonusGamePoolSize");
        Integer bonusSize = (Integer) parameters.get("bonusSize");

        List<Integer> bonusNumbers = randomNumbersGenerator.getRandomCombination(bonusGamePoolSize, bonusSize);

        Integer mainGameSize = (Integer) parameters.get(MAIN_GAME_SIZE);
        Integer mainSystemSize = (Integer) parameters.get(MAIN_SYSTEM_SIZE);
        Integer bonusSystemSize = (Integer) parameters.get(BONUS_SYSTEM_SIZE);

        JsonNode wheelingSystem = combinationBuilder
                .createWheelingCombinations(mainNumbersCombination, bonusNumbers,
                        mainGameSize, mainSystemSize, bonusSize, bonusSystemSize);
        if (LOGGER.isDebugEnabled()) {
            LOGGER.debug(String.format(RETURN_JSON, wheelingSystem.asText()));
        }

        return wheelingSystem;

    }

    /**
     * Performs validation of system before it is processed into a wheeling system, sieves undesirable combinations.
     *
     * @param requestData
     * @return
     */
    public JsonNode getSievedWheelingSystem(JsonNode requestData) {
        ObjectMapper mapper = new ObjectMapper();
        return requestData;
    }

}


